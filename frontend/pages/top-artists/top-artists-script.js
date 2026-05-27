const lang = navigator.language.startsWith("en") ? "en" : "es";

const i18n = {
    es: {
        title: "Tus artistas más escuchados",
        shortTerm: "1 mes",
        mediumTerm: "6 meses",
        longTerm: "1 año",
        logout: "Cerrar sesión"
    },
    en: {
        title: "Your most listened-to artists",
        shortTerm: "1 month",
        mediumTerm: "6 months",
        longTerm: "1 year",
        logout: "Log out"
    }
};

const t = i18n[lang];

document.getElementById("titulo-top").textContent = t.title;
document.getElementById("btn-short").textContent = t.shortTerm;
document.getElementById("btn-medium").textContent = t.mediumTerm;
document.getElementById("btn-long").textContent = t.longTerm;
document.getElementById("logout-btn").textContent = t.logout;

function logout() {
    window.location.href = "/logout";
}
let current_range = "short_term";

async function update_range(range,btn_element){
    current_range = range;
    
    const buttons = document.querySelectorAll('.range-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    if(btn_element) {
        btn_element.classList.add('active');
    }
    loadArtists(current_range);
}

async function loadArtists(range) {
    const response = await fetch(`/api/top-artists?time_range=${range}`, {
        credentials: "include"
    });
    const data = await response.json();

    if (data.error) {
        
        if(data.error == "NO_SESSION"){
            window.location.href = "/?r=no_session";
            return;
        }
        if(data.error == "SESSION_EXPIRED"){
            const refreshed = await tryRefresh();
            if (refreshed.ok) {
                loadArtists(range);
                return;
            }
            if (refreshed.error == "FAILED_TO_REFRESH") {
                window.location.href = "/?r=session_expired";
                return;
            }
            if (refreshed.error == "NO_SESSION") {
                window.location.href = "/?r=no_session";
                return;
            }
            window.location.href = "/?r=error";
            return;
        }
        if(data.error == "FAILED_TO_FETCH_ARTISTS"){
            window.location.href = "/?r=fetch_error";
            return;
        }

        window.location.href = "/?r=error";
        return;
    }
    const container = document.getElementById("artists");
    container.innerHTML = "";
   
    data.forEach(artist => {
        const card = document.createElement("div");
        card.className = "artist-card";
        const image = document.createElement("img");
        image.src = artist.image || "https://via.placeholder.com/150";
        image.alt = artist.name;
        const name = document.createElement("h3");
        name.textContent = artist.name;
        card.appendChild(image);
        card.appendChild(name);
        container.appendChild(card);


    });
    


}

async function tryRefresh() {
    try {
        const response = await fetch("/refresh", { method: "POST", credentials: "include" });
        const data = await response.json();
        if (data.ok) return { ok: true };
        return { ok: false, error: data.error };
    } catch {
        return { ok: false, error: "NETWORK_ERROR" };
    }
}

loadArtists(current_range);