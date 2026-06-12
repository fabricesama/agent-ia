import json

# --- IMPLÉMENTATION DES OUTILS ---

def analyser_cv(nom_candidat: str) -> str:
    """Simule l'extraction et l'analyse textuelle d'un CV."""
    candidats = {
        "alice": "Alice Martin - Développeuse Fullstack (3 ans d'exp). Spécialités: React, Node.js, PostgreSQL. Projet marquant: Refonte d'un CRM.",
        "bob": "Bob Lefebvre - Ingénieur DevOps (5 ans d'exp). Spécialités: Docker, Kubernetes, AWS, CI/CD Jenkins. Certifié AWS Architect.",
        "charlie": "Charlie Dubois - Data Scientist (1 an d'exp). Spécialités: Python, TensorFlow, SQL. Master en Intelligence Artificielle."
    }
    nom_clean = nom_candidat.lower().strip()
    if nom_clean in candidats:
        return f"[OUTIL ANALYSER_CV] Données trouvées pour {nom_candidat}: {candidats[nom_clean]}"
    return f"[OUTIL ANALYSER_CV] Profil de '{nom_candidat}' introuvable dans la base de données des CV."

def evaluer_competences(poste_vise: str, competences_candidat: str) -> str:
    """Compare le profil d'un candidat avec les prérequis d'un poste de manière sécurisée."""
    if not poste_vise or not competences_candidat:
        return "[ERREUR OUTIL] Paramètres manquants pour procéder à l'évaluation."
        
    try:
        # Simulation d'un traitement
        poste_clean = poste_vise.strip()
        return f"[OUTIL EVALUER_COMPETENCES] Analyse pour '{poste_clean}'. Profil adéquat à 85%."
    except Exception as e:
        return f"[ERREUR OUTIL] Échec de l'analyse : {str(e)}"

def generer_questions_entretien(poste: str, niveau: str = "intermédiaire") -> str:
    """Génère des questions techniques et comportementales adaptées."""
    return json.dumps({
        "questions_techniques": [
            f"Pouvez-vous nous parler de votre dernière architecture sur un poste de niveau {niveau} en tant que {poste} ?",
            "Comment gérez-vous la dette technique sur un sprint serré ?"
        ],
        "question_comportementale": "Décrivez une situation où vous étiez en désaccord technique avec un collègue. Comment l'avez-vous résolu ?"
    }, ensure_ascii=False)

# --- MAP DES FONCTIONS ---
OUTILS_DISPONIBLES = {
    "analyser_cv": analyser_cv,
    "evaluer_competences": evaluer_competences,
    "generer_questions_entretien": generer_questions_entretien
}

# --- DÉFINITIONS DES SCHÉMAS (POUR OPENAI) ---
OUTILS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "analyser_cv",
            "description": "Permet de récupérer les détails professionnels, l'expérience et les compétences d'un candidat (ex: Alice, Bob, Charlie) à partir de son nom.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nom_candidat": {"type": "string", "description": "Le prénom ou nom complet du candidat."}
                },
                "required": ["nom_candidat"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluer_competences",
            "description": "Évalue l'adéquation entre les compétences réelles d'un candidat et les exigences d'un poste spécifique.",
            "parameters": {
                "type": "object",
                "properties": {
                    "poste_vise": {"type": "string", "description": "L'intitulé du poste recherché par l'entreprise."},
                    "competences_candidat": {"type": "string", "description": "La liste des compétences ou le résumé du CV du candidat."}
                },
                "required": ["poste_vise", "competences_candidat"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generer_questions_entretien",
            "description": "Génère des questions d'entretien sur-mesure basées sur un poste et un niveau d'expérience.",
            "parameters": {
                "type": "object",
                "properties": {
                    "poste": {"type": "string", "description": "L'intitulé du poste (ex: Développeur, DevOps)."},
                    "niveau": {"type": "string", "enum": ["junior", "intermédiaire", "senior"], "default": "intermédiaire"}
                },
                "required": ["poste"]
            }
        }
    }
]