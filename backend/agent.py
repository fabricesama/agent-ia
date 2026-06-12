import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import OUTILS_SCHEMA, OUTILS_DISPONIBLES

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

SYSTEM_PROMPT = """Tu es 'TalentBot', un agent IA autonome expert en recrutement et ressources humaines.
Tu as pour mission d'aider les recruteurs à analyser des profils, évaluer des compétences et préparer des entretiens.

Consignes strictes :
1. Tu as accès à des outils. Si tu as besoin de données sur un candidat (ex: Alice, Bob, Charlie) ou de questions types, utilise TOUJOURS l'outil approprié d'abord.
2. Formule tes réponses finales avec un ton chaleureux, très professionnel, clair et bien structuré en Markdown.
3. Si un outil renvoie une erreur ou une absence de données, gère-le poliment sans planter.
4. Ne parle jamais de tes outils internes ou du format JSON à l'utilisateur final. Donne directement la synthèse de tes analyses.
"""

def charger_memoire() -> list:
    """Charge l'historique des conversations depuis le fichier JSON."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def sauvegarder_memoire(historique: list):
    """Sauvegarde l'historique dans le fichier JSON (limité aux 20 derniers messages pour optimiser la mémoire)."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(historique[-20:], f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la mémoire : {e}")

def executer_agent_autonome(message_utilisateur: str) -> str:
    """Boucle d'exécution autonome de l'agent (Reasoning + Acting)."""
    historique = charger_memoire()
    
    # Ajout du message utilisateur actuel à l'historique de contexte
    historique.append({"role": "user", "content": message_utilisateur})
    
    # Construction des messages pour l'appel API
    messages_session = [{"role": "system", "content": SYSTEM_PROMPT}] + historique
    
    max_iterations = 5
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"[Agent] Itération de réflexion {iteration}/{max_iterations}...")
        
        try:
            # Appel au LLM
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_session,
                tools=OUTILS_SCHEMA,
                tool_choice="auto"
            )
        except Exception as e:
            return f"⚠️ Erreur de communication avec l'API OpenAI : {str(e)}"
        
        message_ia = response.choices[0].message
        
        # Enregistrement de la réflexion de l'IA dans la session actuelle
        messages_session.append(message_ia)
        
        # Vérification : L'IA veut-elle appeler un outil ?
        if message_ia.tool_calls:
            for tool_call in message_ia.tool_calls:
                nom_fonction = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                print(f"[Agent] Décision : Appel de l'outil '{nom_fonction}' avec {arguments}")
                
                # Exécution sécurisée de l'outil
                if nom_fonction in OUTILS_DISPONIBLES:
                    try:
                        resultat_outil = OUTILS_DISPONIBLES[nom_fonction](**arguments)
                    except Exception as err:
                        resultat_outil = f"Erreur critique lors de l'exécution de l'outil : {str(err)}"
                else:
                    resultat_outil = f"Erreur : L'outil {nom_fonction} n'existe pas."
                
                # On réinjecte le résultat de l'outil dans le flux de la conversation
                messages_session.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": nom_fonction,
                    "content": resultat_outil
                })
            # La boucle continue pour laisser le LLM prendre connaissance du résultat de l'outil
            continue
        
        # Si aucun outil n'est demandé, c'est la réponse finale !
        else:
            # On met à jour l'historique persistant avec l'échange final
            historique.append({"role": "assistant", "content": message_ia.content})
            sauvegarder_memoire(historique)
            return message_ia.content
            
    return "⚠️ L'agent a été arrêté par sécurité : limite maximale de réflexion atteinte sans réponse finale."

def executer_agent_autonome_detaille(message_utilisateur: str) -> dict:
    historique = charger_memoire()
    historique.append({"role": "user", "content": message_utilisateur})
    messages_session = [{"role": "system", "content": SYSTEM_PROMPT}] + historique
    
    max_iterations = 5
    iteration = 0
    logs_outils = [] # Pour stocker les actions de l'agent
    
    while iteration < max_iterations:
        iteration += 1
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_session,
            tools=OUTILS_SCHEMA,
            tool_choice="auto"
        )
        message_ia = response.choices[0].message
        messages_session.append(message_ia)
        
        if message_ia.tool_calls:
            for tool_call in message_ia.tool_calls:
                nom_fonction = tool_call.function.name
                # On enregistre l'action pour le frontend
                logs_outils.append(f"🔧 Utilisation de l'outil : <strong>{nom_fonction}</strong>")
                
                arguments = json.loads(tool_call.function.arguments)
                if nom_fonction in OUTILS_DISPONIBLES:
                    try:
                        resultat_outil = OUTILS_DISPONIBLES[nom_fonction](**arguments)
                    except Exception as err:
                        resultat_outil = f"Erreur : {str(err)}"
                else:
                    resultat_outil = "Outil introuvable."
                
                messages_session.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": nom_fonction,
                    "content": resultat_outil
                })
            continue
        else:
            historique.append({"role": "assistant", "content": message_ia.content})
            sauvegarder_memoire(historique)
            return {"response": message_ia.content, "logs": logs_outils}
            
    return {"response": "Limite atteinte.", "logs": logs_outils}