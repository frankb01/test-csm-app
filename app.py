import streamlit as st
from openai import OpenAI
from st_audiorec import st_audiorec
import os

# Configuration UI
st.set_page_config(page_title="CSM Coach AI", page_icon="🚀")
st.title("🚀 Simulateur d'Entretien CSM Expert")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Prompt Système Intégré
SYSTEM_PROMPT = """
Tu es un recruteur senior CSM. Évalue le candidat sur :
1. Diagnostic Data & ROI. 2. Empathie & Gestion du Churn. 3. Méthode STAR.
4. Éloquence : Repère les tics ('euh', 'du coup', 'petit') et suggère des alternatives pro.
Pose une question à la fois. Après 5 questions, donne un score sur 20 et un débriefing détaillé.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Affichage des messages
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Capturer l'audio
st.write("### 🎙️ Répondez à la voix")
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    with st.spinner("Analyse de votre réponse..."):
        # 1. Transcription Whisper
        with open("temp_audio.wav", "wb") as f:
            f.write(wav_audio_data)
        
        with open("temp_audio.wav", "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        
        # 2. Mise à jour de la conversation
        st.session_state.messages.append({"role": "user", "content": transcript})
        
        # 3. Réponse du Recruteur
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        ai_txt = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_txt})
        st.rerun()

# Option de secours par texte
if prompt := st.chat_input("Ou tapez votre réponse ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
