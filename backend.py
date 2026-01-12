from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

# Chargement des variables
load_dotenv()

app = FastAPI()

# Initialisation des clients
client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
model_embedding = SentenceTransformer('all-MiniLM-L6-v2')

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask(req: QueryRequest):
    print(f"📩 Question étudiante reçue : {req.question}")
    
    # 1. On récupère quand même le contexte du cours
    # Pourquoi ? Pour que le tuteur sache de quelle méthode on parle dans CE cours spécifique.
    xq = model_embedding.encode(req.question).tolist()
    res = index.query(vector=xq, top_k=3, include_metadata=True)
    
    course_context = ""
    for match in res['matches']:
        if 'text' in match['metadata']:
            course_context += match['metadata']['text'] + "\n---\n"
    
    # 2. LE COEUR DU CHANGEMENT : Le Prompt "Tuteur Socratique"
    system_prompt = """
    Tu es un Professeur Assistant expert et pédagogue.
    Ton objectif est d'aider l'étudiant à COMPRENDRE et RAISONNER, pas de lui donner la solution.
    
    Tu as accès à des extraits du cours (Contexte), mais tu ne dois pas simplement les recopier.
    
    RÈGLES STRICTES DE COMPORTEMENT :
    1. 🚫 NE DONNE JAMAIS LA RÉPONSE FINALE ou le résultat direct (sauf si c'est une pure définition).
    2. 🧠 Décompose le problème : Propose une méthodologie étape par étape.
    3. ❓ Pose des questions : Si l'étudiant est bloqué, pose-lui une question pour le guider vers la prochaine étape.
    4. 📚 Utilise le contexte fourni pour t'assurer que ta méthode correspond à ce qui est enseigné dans le cours, mais reformule-le avec tes propres mots.
    5. Si la question demande du code, donne la structure ou les commentaires, mais laisse des "trous" à remplir par l'étudiant.
    6. Sois encourageant, mais ferme sur le fait de ne pas faire le travail à sa place.
    
    Exemple : Si l'étudiant demande "C'est quoi la dérivée de x^2 ?", ne dis pas "2x". Dis plutôt : "Rappelle-toi de la règle de dérivation des puissances (nx^n-1). Ici, que vaut n ?"
    """
    
    # 3. Envoi à l'IA (Groq)
    completion = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile", # Modèle puissant nécessaire pour suivre ces règles complexes
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contexte du cours (à utiliser pour la méthode) : {course_context}\n\nQuestion de l'étudiant : {req.question}"}
        ],
        temperature=0.4 # Un peu de créativité pour la pédagogie, mais pas trop
    )
    
    answer = completion.choices[0].message.content
    
    # On renvoie la réponse + les sources (pour que le prof voie que tu utilises la DB)
    return {"answer": answer, "sources": course_context}