const API_URL = "http://127.0.0.1:8000/api";

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");

// Événement d'envoi
sendBtn.addEventListener("click", envoyerMessage);
userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") envoyerMessage();
});

// Réinitialisation de l'historique
clearBtn.addEventListener("click", async () => {
    if (confirm("Voulez-vous vraiment vider la mémoire de l'agent ?")) {
        try {
            await fetch(`${API_URL}/memory`, { method: "DELETE" });
            chatBox.innerHTML = "";
            ajouterMessage("bot", "Mémoire réinitialisée ! Mon historique conversationnel est propre.");
        } catch (error) {
            console.error("Erreur lors du clear :", error);
        }
    }
});

async function envoyerMessage() {
    const texte = userInput.value.trim();
    if (!texte) return;

    // 1. Afficher le message de l'utilisateur
    ajouterMessage("user", texte);
    userInput.value = "";

    // 2. Créer et afficher le conteneur du loader pour faire patienter pendant la boucle ReAct
    const loaderId = ajouterLoader();
    scrollBottom();

    try {
        // 3. Appel HTTP POST au serveur FastAPI
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: texte })
        });

        const data = await response.json();
        
        // Supprimer le loader d'attente
        retirerLoader(loaderId);

        if (data.success) {
            // 4. Affichage de la réponse finale stylisée avec Marked.js (Markdown)
            ajouterMessage("bot", data.response);
        } else {
            ajouterMessage("bot", "❌ Désolé, une erreur technique est survenue sur le serveur.");
        }

    } catch (error) {
        retirerLoader(loaderId);
        ajouterMessage("bot", "❌ Impossible de joindre le serveur. Assurez-vous que le backend FastAPI est lancé.");
        console.error("Erreur Fetch :", error);
    }

    scrollBottom();
}

function ajouterMessage(auteur, message) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", `${auteur}-message`);

    const avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.innerText = auteur === "user" ? "👨‍💼" : "🤖";

    const content = document.createElement("div");
    content.classList.add("content");
    
    if (auteur === "bot") {
        // Parse le Markdown uniquement pour l'IA
        content.innerHTML = marked.parse(message);
    } else {
        content.innerText = message;
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatBox.appendChild(messageDiv);
    scrollBottom();
}

function ajouterLoader() {
    const id = "loader-" + Date.now();
    const loaderDiv = document.createElement("div");
    loaderDiv.classList.add("message", "bot-message");
    loaderDiv.setAttribute("id", id);

    loaderDiv.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="content">
            <div class="loading-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatBox.appendChild(loaderDiv);
    return id;
}

function retirerLoader(id) {
    const loader = document.getElementById(id);
    if (loader) loader.remove();
}

function scrollBottom() {
    const wrapper = document.querySelector(".chat-wrapper");
    wrapper.scrollTop = wrapper.scrollHeight;
}

function ajouterMessageSysteme(texte) {
    const logDiv = document.createElement("div");
    logDiv.classList.add("system-log");
    logDiv.innerHTML = texte;
    chatBox.appendChild(logDiv);
}