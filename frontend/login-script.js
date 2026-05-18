function login() {
    window.location.href = "/login";
}

function showToast(message){
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 2500);
}

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const reason = params.get("r");
    
    if (reason === "session_expired") {
        showToast("Tu sesión expiró, volvé a iniciar sesión");
        window.history.replaceState({}, "", "/");
    } else if (reason === "fetch_error") {
        showToast("No se pudieron cargar tus artistas, intentá nuevamente");
        window.history.replaceState({}, "", "/");
    }
    else if (reason === "error") {
        showToast("Algo salió mal, intentá nuevamente");
        window.history.replaceState({}, "", "/");
    }
});

