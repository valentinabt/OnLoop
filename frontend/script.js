function login() {
    window.location.href = "http://127.0.0.1:8000/login";
}

function logout() {
    window.location.href = "http://127.0.0.1:8000/logout";
}

async function loadArtists() {
    const response = await fetch("http://127.0.0.1:8000/top-artists", {
        credentials: "include"
    });
    const data = await response.json();

    if (data.error) {
        document.getElementById("home").style.display = "flex";
        document.getElementById("top").style.display = "none";
        return;
    }

    const container = document.getElementById("artists");
    container.innerHTML = "";

    data.forEach(artist => {
        container.innerHTML += `
            <div class="artist-card">
                <img src="${artist.image || 'https://via.placeholder.com/150'}" alt="${artist.name}">
                <h3>${artist.name}</h3>
            </div>
        `;
    });

    document.getElementById("home").style.display = "none";
    document.getElementById("top").style.display = "flex";
    document.title = "Tu top 10 - Toptify";
}

loadArtists();