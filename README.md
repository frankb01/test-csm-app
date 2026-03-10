🚀 CSM Interview Coach AI
Simulateur d'entretien d'embauche intelligent pour Customer Success Managers (CSM).

Ce projet utilise l'IA pour simuler un entretien réaliste, évaluer tes compétences stratégiques (Churn, ROI, KPIs) et analyser ton éloquence en temps réel.

✨ Fonctionnalités
🎙️ Entrée Vocale : Réponds aux questions à haute voix grâce à l'intégration de OpenAI Whisper.

🧠 Intelligence Métier : Scénarios spécifiques au CSM (Gestion de crise, QBR, expansion de compte).

📊 Analyse STAR : Vérification de la structure de tes réponses.

🚫 Détecteur de Tics de Langage : Identification des "euh", "du coup" et conseils pour une posture de "Conseiller de confiance".

🏆 Score Final : Débriefing complet avec une note sur 20.

🛠️ Technologies utilisées
Framework : Streamlit

LLM : OpenAI GPT-4o

Speech-to-Text : OpenAI Whisper

Langage : Python 3.9+

🚀 Installation locale
Cloner le dépôt :

Bash
git clone https://github.com/frankb01/test-csm-app.git
cd csm-ai-coach
Installer les dépendances :

Bash
pip install -r requirements.txt
Configurer les secrets :
Créez un fichier .streamlit/secrets.toml et ajoutez votre clé :

Ini, TOML
OPENAI_API_KEY = "votre_cle_ici"
Lancer l'application :

Bash
streamlit run app.py
📝 Structure du projet
Plaintext
.
├── app.py              # Code principal de l'application Streamlit
├── requirements.txt    # Liste des bibliothèques Python
└── README.md           # Documentation du projet
🤝 Contribution
Les contributions sont les bienvenues ! Si vous avez des idées de scénarios CSM (ex: renouvellement difficile), n'hésitez pas à ouvrir une Issue ou une Pull Request.
