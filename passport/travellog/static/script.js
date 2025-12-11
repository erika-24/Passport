// Initialize map
const map = L.map("map").setView([20, 0], 2);

// Base tiles
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
}).addTo(map);

const bounds = [];

// Add markers from Django data
destinations.forEach(d => {
    const marker = L.circleMarker([d.lat, d.lng], {
        radius: 6,
        color: d.visited ? "#16a34a" : "#2563eb",
        fillColor: d.visited ? "#16a34a" : "#2563eb",
        fillOpacity: 0.9
    }).addTo(map);

    marker.bindPopup(`<b>${d.name}</b><br>${d.visited ? "Visited" : "Planned"}`);

    bounds.push([d.lat, d.lng]);
});

// Auto-fit map to markers
if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [40, 40] });
}

// Modal logic
const openBtn = document.getElementById("open-add-trip");
const closeBtn = document.getElementById("close-add-trip");
const overlay = document.getElementById("add-trip-overlay");

if (openBtn && closeBtn && overlay) {
    // Open modal
    openBtn.addEventListener("click", () => {
        overlay.classList.remove("hidden");
    });

    // Close modal via X button
    closeBtn.addEventListener("click", () => {
        overlay.classList.add("hidden");
    });

    // Close modal when clicking outside the modal box
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) {
            overlay.classList.add("hidden");
        }
    });

    // Close with Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            overlay.classList.add("hidden");
        }
    });
}

// Journal modal logic
const openJournalBtn = document.getElementById("open-journal-modal");
const closeJournalBtn = document.getElementById("close-journal-modal");
const journalOverlay = document.getElementById("journal-overlay");

if (openJournalBtn && closeJournalBtn && journalOverlay) {
    openJournalBtn.addEventListener("click", () => {
        journalOverlay.classList.remove("hidden");
    });

    closeJournalBtn.addEventListener("click", () => {
        journalOverlay.classList.add("hidden");
    });

    journalOverlay.addEventListener("click", (e) => {
        if (e.target === journalOverlay) {
            journalOverlay.classList.add("hidden");
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            journalOverlay.classList.add("hidden");
        }
    });
}

// Render rating stars for journal entries
document.querySelectorAll(".journal-rating").forEach((el) => {
    const rating = parseInt(el.dataset.rating || "0", 10);
    const max = 5;
    const filled = "★".repeat(Math.max(0, Math.min(rating, max)));
    const empty = "☆".repeat(Math.max(0, max - rating));
    el.textContent = filled + empty;
});
