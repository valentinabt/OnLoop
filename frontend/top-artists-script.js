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
        
        if(error == "NO_ACTIVE_SESSION"){
            window.location.href = "/login?r=session_expired";
            
        }
        window.location.href = "/login?r=error";
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


loadArtists(current_range);