// Ensure data is loaded
let data = [];
if (typeof locationsData !== 'undefined') {
    data = locationsData;
} else {
    console.error("locationsData is not defined. Ensure data.js is loaded correctly.");
}

// Initialize Map
const map = L.map('map', {
    zoomControl: false // Move zoom control
}).setView([41.8719, 12.5674], 6); // Center of Italy

// Add Zoom Control to bottom right
L.control.zoom({
    position: 'bottomright'
}).addTo(map);

// Add Tile Layer (OpenStreetMap)
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
}).addTo(map);

const createCustomIcon = (sezione, isBoth) => {
    let colorClass = 'icon-' + sezione;
    if (isBoth) {
        colorClass = 'icon-both';
    }
    
    return L.divIcon({
        className: `custom-marker ${colorClass}`,
        html: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>`,
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
};

const markers = []; // Store all markers for filtering

// Add Markers
data.forEach(loc => {
    if (loc.lat && loc.lon) {
        const icon = createCustomIcon(loc.sezione, loc.sezione_both);
        const marker = L.marker([loc.lat, loc.lon], { icon: icon }).addTo(map);
        
        // Save metadata for filtering
        marker.sezione = loc.sezione;
        markers.push(marker);
        
        if (loc.sezione === 'II' || (loc.sezione === 'I' && loc.subsections && loc.subsections.length > 0)) {
            // Clusters and Museums use the detailed modal
            marker.on('click', () => openMuseumModal(loc));
        } else {
            // Build Popup Content for normal markers
            let popupHtml = `<div class="popup-content">`;
            
            if (loc.image) {
                popupHtml += `<img src="${loc.image}" alt="${loc.name}" class="popup-img">`;
            }
            
            popupHtml += `<div class="popup-info">`;
            popupHtml += `<div class="popup-region">${loc.region}</div>`;
            if (loc.exam_id) {
                popupHtml += `<span style="background:var(--primary);color:white;padding:2px 6px;border-radius:4px;font-size:0.75rem;font-weight:bold;margin-bottom:0.5rem;display:inline-block;">ID: ${loc.exam_id}</span>`;
            }
            popupHtml += `<h3 class="popup-title">${loc.name}</h3>`;
            
            if (loc.sezione_both) {
                popupHtml += `<div style="background:#fef2f2; color:#b91c1c; padding:0.5rem; border-radius:4px; margin-bottom:0.5rem; font-size:0.85rem; border-left:3px solid #ef4444;">
                    <strong>⚠️ Attenzione:</strong> Questo sito è fondamentale. Fa parte sia della Sezione I (Prova Scritta) che della Sezione III (Orale).
                </div>`;
            }

            if (loc.extract) {
                popupHtml += `<p class="popup-desc">${loc.extract}</p>`;
            }
            
            if (loc.url) {
                popupHtml += `<a href="${loc.url}" target="_blank" class="popup-btn">Approfondisci su Wikipedia</a>`;
            }
            
            popupHtml += `</div></div>`;
            
            marker.bindPopup(popupHtml, {
                maxWidth: 320,
                minWidth: 320,
                className: 'custom-popup'
            });
        }
    }
});

// Modal Logic
const modal = document.getElementById('modal-legislazione');
const btnOpen = document.getElementById('btn-legislazione');
const btnClose = document.getElementById('btn-close-modal');

const openModal = () => {
    modal.classList.remove('hidden');
};

const closeModal = () => {
    modal.classList.add('hidden');
};

btnOpen.addEventListener('click', openModal);
btnClose.addEventListener('click', closeModal);

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// Museum Modal Logic
const museumModal = document.getElementById('modal-museum');
const btnCloseMuseum = document.getElementById('btn-close-museum');

// Filter Logic
const btnFiltroScritto = document.getElementById('btn-filtro-scritto');
let isFilterActive = false;

btnFiltroScritto.addEventListener('click', () => {
    isFilterActive = !isFilterActive;
    
    if (isFilterActive) {
        btnFiltroScritto.classList.add('active');
        btnFiltroScritto.innerText = '✅ Mostrando solo Prova Scritta';
        // Hide Sezione III markers
        markers.forEach(m => {
            if (m.sezione === 'III') {
                map.removeLayer(m);
            }
        });
    } else {
        btnFiltroScritto.classList.remove('active');
        btnFiltroScritto.innerText = '🎯 Solo Prova Scritta';
        // Show all markers
        markers.forEach(m => {
            if (!map.hasLayer(m)) {
                m.addTo(map);
            }
        });
    }
});

const openMuseumModal = (loc) => {
    // Populate header
    document.getElementById('museum-title').innerHTML = loc.name + (loc.exam_id ? ` <span style="background:var(--primary);color:white;padding:4px 8px;border-radius:4px;font-size:0.85rem;vertical-align:middle;margin-left:8px;">ID: ${loc.exam_id}</span>` : '');
    document.getElementById('museum-main-desc').innerHTML = loc.extract || 'Nessuna descrizione disponibile.';
    
    const linkObj = document.getElementById('museum-main-link');
    if (loc.url) {
        linkObj.href = loc.url;
        linkObj.style.display = 'inline-block';
    } else {
        linkObj.style.display = 'none';
    }

    const mainImg = document.getElementById('museum-main-img');
    if (loc.image) {
        mainImg.src = loc.image;
        mainImg.classList.remove('hidden');
    } else {
        mainImg.classList.add('hidden');
    }

    // Populate subsections
    const subContainer = document.getElementById('museum-subsections-container');
    const subTitle = document.getElementById('museum-subsections-title');
    subContainer.innerHTML = '';
    
    if (loc.subsections && loc.subsections.length > 0) {
        subTitle.classList.remove('hidden');
        loc.subsections.forEach(sub => {
            const card = document.createElement('div');
            card.className = 'subsection-card';
            
            let html = '';
            if (sub.image) {
                html += `<img src="${sub.image}" class="subsection-img" alt="${sub.name}">`;
            } else {
                html += `<div class="subsection-img" style="display:flex;align-items:center;justify-content:center;color:#94a3b8;"><svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg></div>`;
            }
            
            html += `<div class="subsection-info">`;
            html += `<h4>${sub.name}</h4>`;
            if (sub.extract) {
                html += `<p>${sub.extract}</p>`;
            }
            if (sub.url) {
                html += `<a href="${sub.url}" target="_blank" class="btn-link" style="font-size:0.85rem;">Vedi su Wiki</a>`;
            }
            html += `</div>`;
            
            card.innerHTML = html;
            subContainer.appendChild(card);
        });
    } else {
        subTitle.classList.add('hidden');
        subContainer.innerHTML = '<p style="color:var(--text-muted)">Nessuna sottosezione specificata per questo museo.</p>';
    }

    museumModal.classList.remove('hidden');
};

const closeMuseumModal = () => {
    museumModal.classList.add('hidden');
};

btnCloseMuseum.addEventListener('click', closeMuseumModal);

museumModal.addEventListener('click', (e) => {
    if (e.target === museumModal) {
        closeMuseumModal();
    }
});

// Close all modals on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (!modal.classList.contains('hidden')) closeModal();
        if (!museumModal.classList.contains('hidden')) closeMuseumModal();
    }
});
