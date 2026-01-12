🎓 StudyGuide AI 

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Groq](https://img.shields.io/badge/AI-Groq-orange)

##  Description du Projet
StudyGuide AI est une application éducative innovante développée dans le cadre du Master à l'Université Internationale de Rabat. 

Contrairement aux chatbots classiques qui donnent directement les réponses. Il utilise le contenu réel du cours pour guider l'étudiant vers la solution par le questionnement et la méthodologie, sans jamais faire l'exercice à sa place.

##  Architecture Technique
L'application suit une architecture RAG  moderne :

1.  **Ingestion :** Les cours (PDF) sont vectoriséset stockés dans **Pinecone**.
2.  **Backend (FastAPI) :** Gère la logique et l'interrogation de la base vectorielle.
3.  **Intelligence (Groq) :** Utilise le modèle `llama-3.3-70b` avec un prompt système strict pour forcer le comportement pédagogique.
4.  **Frontend (Streamlit) :** Interface utilisateur simple pour les étudiants.

## 🚀 Installation et Démarrage

### 1. Cloner le projet
```bash
git clone [https://github.com/haytamheh-web/tuteur.git](https://github.com/haytamheh-web/tuteur.git)
cd tuteur
