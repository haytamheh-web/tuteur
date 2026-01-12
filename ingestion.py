import os
import time
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from dotenv import load_dotenv
import uuid

# Chargement
load_dotenv()
print("⏳ Chargement du modèle IA (peut prendre 30s la première fois)...")
model = SentenceTransformer('all-MiniLM-L6-v2') # Modèle léger et gratuit

# Connexion Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

# Créer l'index s'il n'existe pas
if index_name not in [idx.name for idx in pc.list_indexes()]:
    print(f"📍 Création de l'index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=384,  # Dimension du modèle all-MiniLM-L6-v2
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    print("⏳ Attente de la création de l'index (environ 10-20 secondes)...")
    time.sleep(15)  # Attendre que l'index soit prêt

index = pc.Index(index_name)

def get_pdf_text(folder):
    text = ""
    for filename in os.listdir(folder):
        if filename.endswith('.pdf'):
            print(f"   📄 Lecture de : {filename}")
            reader = PdfReader(os.path.join(folder, filename))
            for page in reader.pages:
                text += page.extract_text() or ""
    return text

def run_ingestion():
    print("🚀 Démarrage de l'ingestion...")
    
    # 1. Lire les PDF
    raw_text = get_pdf_text("documents")
    if not raw_text:
        print("❌ Erreur : Aucun texte trouvé dans le dossier 'documents'.")
        return

    # 2. Découper en morceaux (Chunks)
    chunk_size = 500
    chunks = [raw_text[i:i+chunk_size] for i in range(0, len(raw_text), chunk_size)]
    print(f"✂️  Texte découpé en {len(chunks)} morceaux.")

    # 3. Vectoriser et envoyer
    vectors = []
    print("🧠 Vectorisation en cours...")
    embeddings = model.encode(chunks)
    
    for i, chunk in enumerate(chunks):
        vectors.append({
            "id": str(uuid.uuid4()),
            "values": embeddings[i].tolist(),
            "metadata": {"text": chunk}
        })

    # Envoi par paquets de 100
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        index.upsert(vectors=batch)
        print(f"   cloud ☁️  Paquet {i//batch_size + 1} envoyé.")

    print("✅ Terminé ! Ta base de données est prête.")

if __name__ == "__main__":
    run_ingestion()