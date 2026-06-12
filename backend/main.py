import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import executer_agent_autonome, charger_memoire, sauvegarder_memoire

load_dotenv()

app = FastAPI(title="TalentBot API", description="Backend pour l'agent autonome de recrutement")

# Configuration CORS pour que le Frontend HTML puisse appeler le Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle de données pour les requêtes entrantes
class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Le message ne peut pas être vide.")
    
    try:
        # On va intercepter ce qu'il s'est passé dans l'agent
        # On modifie légèrement le retour de l'agent pour obtenir un dictionnaire
        resultat = executer_agent_autonome_detaille(payload.message)
        return {
            "success": True, 
            "response": resultat["response"], 
            "logs": resultat["logs"] # Liste des outils appelés
        }
    except Exception as e:
        return {"success": False, "response": f"Une erreur interne est survenue : {str(e)}", "logs": []}

@app.delete("/api/memory")
async def clear_memory():
    """Endpoint utilitaire pour réinitialiser la mémoire de l'agent si besoin."""
    sauvegarder_memoire([])
    return {"success": True, "message": "Mémoire réinitialisée."}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)