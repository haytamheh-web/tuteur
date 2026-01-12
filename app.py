import streamlit as st
import requests

st.set_page_config(page_title="IA Tuteur", page_icon="🎓")

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
                    
                else:
                    st.error("Erreur Backend.")
            except Exception as e:
                st.error(f"Impossible de joindre le serveur. Vérifie que 'backend.py' tourne. Erreur: {e}")