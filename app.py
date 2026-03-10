import streamlit as st
from openai import OpenAI
from st_audiorec import st_audiorec
import os

# 1. Configuration et Style
st.set_page_config(page_title="CSM Coach AI", page_icon="🚀", layout="centered")
st.title("🚀 Simulateur d'Entretien CSM")

# 2. Initialisation Client
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Clé API manquante dans les Secrets Streamlit !")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. Système de mémoire (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """Tu es un recruteur senior CSM. 
        - Pose UNE SEULE question à la fois.
        - Attends TOUJOURS la réponse du candidat avant de continuer.
        - Analyse les tics de langage ('euh', 'du coup', 'petit').
        - Après 5 questions, donne un score sur 20 et un débriefing.""" }
    ]

# 4. Affichage de l'historique (sauf le prompt système)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- LOGIQUE DE TOUR PAR TOUR ---
last_role = st.session_state.messages[-1]["role"]

# A. Si c'est au tour de l'IA de parler (après le système ou après l'utilisateur)
if last_role in ["system", "user"]:
    with st.chat_message("assistant"):
        with st.spinner("Le recruteur prépare sa question..."):
            response = client.chat.completions.create(
                model="gpt-4o", # Ou "gpt-4o-mini" pour économiser
                messages=st.session_state.messages
            )
            ai_txt = response.choices[0].message.content
            st.markdown(ai_txt)
            st.session_state.messages.append({"role": "assistant", "content": ai_txt})
            st.rerun() # Relance pour afficher les widgets de réponse

# B. Si c'est au tour de l'Utilisateur (le dernier message est 'assistant')
else:
    st.divider()
    st.write("### 🎙️ Votre réponse")
    
    # Widget Audio
    wav_audio_data = st_audiorec()
    
    # Widget Texte (au cas où)
    text_input = st.chat_input("Ou répondez par écrit ici...")

    # Traitement de l'Audio
    if wav_audio_data is not None:
        # On vérifie que le fichier n'est pas vide (buffer de sécurité)
        if len(wav_audio_data) > 5000:
            with st.spinner("Transcription de votre voix..."):
                with open("temp_audio.wav", "wb") as f:
                    f.write(wav_audio_data)
                
                with open("temp_audio.wav", "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file,
                        response_format="text"
                    )
                
                if transcript.strip():
                    st.session_state.messages.append({"role": "user", "content": transcript})
                    st.rerun()

    # Traitement du Texte
    if text_input:
        st.session_state.messages.append({"role": "user", "content": text_input})
        st.rerun()
