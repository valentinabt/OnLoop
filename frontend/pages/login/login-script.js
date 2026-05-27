const lang = navigator.language.startsWith("en") ? "en" : "es";


const i18n = {
    es: {
        title: "OnLoop",
        description: "Descubrí tus artistas más escuchados en Spotify",
        loginBtn: "Conectar con Spotify",
        toasts: {
            no_session: "Por favor, inicie sesión",
            fetch_error: "No se pudieron cargar tus artistas, intentá nuevamente",
            session_expired: "Tu sesión ha expirado, por favor inicie sesión nuevamente",
            error: "Algo salió mal, intentá nuevamente"
        }
    },
    en: {
        title: "OnLoop",
        description: "Discover your most listened-to artists on Spotify",
        loginBtn: "Connect with Spotify",
        toasts: {
            no_session: "Please log in",
            fetch_error: "Could not load your artists, please try again",
            session_expired: "Your session has expired, please log in again",
            error: "Something went wrong, please try again"
        }
    }
};

const t = i18n[lang];


function login() {
    window.location.href = "/login";
}

function showToast(message){
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {toast.remove(); }, 3000);
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("description").textContent = t.description;
    document.getElementById("login-btn").textContent = t.loginBtn;


    const params = new URLSearchParams(window.location.search);
    const reason = params.get("r");
    
    if (reason && t.toast[reason]){
        showToast(t.toasts[reason]);
        window.history.replaceState({}, "","/");
    }
});

