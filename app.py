import streamlit as st
from openai import OpenAI
from st_audiorec import st_audiorec
import os

# 1. Configuration de la page
st.set_page_config(page_title="CSM Coach AI", page_icon="🚀", layout="centered")
st.title("🚀 Simulateur d'Entretien CSM")

# 2. Initialisation du Client OpenAI
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Clé API manquante dans les Secrets Streamlit !")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Initialisation de la mémoire (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """Tu es un recruteur senior CSM expert. 
        - Pose UNE SEULE question à la fois.
        - Attends TOUJOURS la réponse du candidat avant de continuer.
        - Analyse la précision des réponses (STAR, KPI, ROI).
        - Analyse l'éloquence : repère les tics ('euh', 'du coup', 'en fait', 'petit').
        - Après 5 questions, donne un score sur 20 et un débriefing complet.""" }
    ]

# --- 4. AFFICHAGE DE LA CONVERSATION ---
# On affiche tout l'historique mémorisé avant de décider de la suite
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- 5. LOGIQUE DE DÉCISION DU TOUR ---
last_role = st.session_state.messages[-1]["role"]

if last_role in ["system", "user"]:
    # C'est au tour de l'IA de générer la question
    with st.chat_message("assistant"):
        with st.spinner("Le recruteur prépare sa question..."):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            ai_txt = response.choices[0].message.content
            # On enregistre le message
            st.session_state.messages.append({"role": "assistant", "content": ai_txt})
            # On force le rafraîchissement pour que la boucle d'affichage (étape 4) montre la question
            st.rerun()

else:
    # C'est au tour de l'UTILISATEUR (le dernier message est celui de l'IA)
    st.divider()
    st.write("### 🎙️ Votre
