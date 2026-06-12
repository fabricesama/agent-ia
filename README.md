# TalentBot - Agent IA Autonome de Recrutement

## 👥 Membres du projet
- SAMA Fabrice-Ertone

## 🎯 Thématique choisie
**TalentBot** est un agent conversationnel autonome conçu pour épauler les équipes de Ressources Humaines. Grâce à une boucle de réflexion autonome (ReAct), il est capable d'analyser des profils de candidats, d'évaluer l'adéquation avec une fiche de poste et de générer des questions techniques pour préparer les entretiens.

## 🛠️ Outils implémentés
1. `analyser_cv` : Extrait le profil complet d'un candidat connu (Alice, Bob, Charlie) depuis notre base de données.
2. `evaluer_competences` : Compare les compétences d'un profil avec les exigences d'un poste donné.
3. `generer_questions_entretien` : Formule des questions de screening sur-mesure selon le niveau d'expérience requis.

## 💾 Fonctionnalités techniques validées
- **Boucle autonome** avec une sécurité fixée à 5 itérations maximum pour éviter les boucles infinies de tokens.
- **Mémoire persistante** locale sauvegardée dans un fichier `memory.json`.
- **Interface Web moderne** avec affichage du Markdown (grâce à Marked.js) et logs d'exécution de l'agent en temps réel.
- **Gestion stricte des erreurs** pour empêcher les crashs serveur (FastAPI + blocs Try/Except sur les outils).

## 🚀 Installation et Lancement

### 1. Prérequis
- Python 3.10 ou supérieur
- Un navigateur web moderne

### 2. Installation des dépendances
```bash
pip install fastapi uvicorn openai python-dotenv pydantic# agent-ia
