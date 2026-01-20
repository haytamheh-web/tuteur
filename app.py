import streamlit as st
import requests
import os

st.set_page_config(page_title="IA Tuteur", page_icon="🎓")

# --- 1. BARRE LATÉRALE : UPLOAD DE DOCUMENTS ---
with st.sidebar:
    st.header("📂 Ajouter un document")
    st.write("Ajoute un cours (PDF) pour enrichir la base de connaissances.")
    
    uploaded_file = st.file_uploader("Choisir un fichier PDF", type="pdf")
    
    if uploaded_file is not None:
        # Nom du dossier de sauvegarde (relatif à ton projet)
        save_folder = "documents"
        
        # Création du dossier s'il n'existe pas
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
            
        # Chemin complet du fichier
        file_path = os.path.join(save_folder, uploaded_file.name)
        
        # Sauvegarde physique du fichier sur le disque
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"✅ Fichier '{uploaded_file.name}' enregistré !")
        st.warning("⚠️ N'oublie pas de relancer 'ingestion.py' pour que l'IA lise ce nouveau fichier.")

# --- 2. ZONE PRINCIPALE : CHATBOT ---
st.title("🎓 Study Guide IA")
st.info("Pose une question sur ton cours, je t'aiderai à trouver la réponse sans tricher !")

question = st.text_area("Ta question :", height=100)

if st.button("Demander de l'aide"):
    if not question:
        st.warning("Écris quelque chose d'abord.")
    else:
        with st.spinner("Analyse en cours..."):
            try:
                # Appel au backend local
                resp = requests.post("http://127.0.0.1:8000/ask", json={"question": question})
                
                if resp.status_code == 200:
                    data = resp.json()
                    st.markdown("### 💡 Guide de l'assistant")
                    st.write(data["answer"])
                    
                    # Optionnel : Afficher les sources si le backend les renvoie
                    if "sources" in data:
                        with st.expander("Voir les sources utilisées"):
                            st.text(data["sources"])
                    elif "context_used" in data:
                         with st.expander("Voir les sources utilisées"):
                            st.text(data["context_used"])

                else:
                    st.error("Erreur Backend.")
            except Exception as e:
                st.error(f"Impossible de joindre le serveur. Vérifie que 'backend.py' tourne. Erreur: {e}")