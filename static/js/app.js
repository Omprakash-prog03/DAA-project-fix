// EV Grid Product-Grade UI Logic
document.addEventListener('DOMContentLoaded', () => {
    console.log("EV Grid Intelligence Platform Initialized");
    
    // Initialize Map (Placeholder for Leaflet/MapLibre)
    // In production, this would load the real map provider
    
    // Handle Sidebar Navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            navItems.forEach(n => n.classList.remove('active'));
            e.target.classList.add('active');
            // Route logic would go here
        });
    });

    // Fetch real data from backend
    fetch('/api/dataset/small_network')
        .then(res => res.json())
        .then(data => {
            if(data.nodes) {
                console.log("Loaded dataset with", data.nodes.length, "nodes");
                // Update UI metrics
                document.querySelector('.metric-card .value').innerText = data.nodes.length;
            }
        })
        .catch(err => console.error("Offline Demo Mode / API Unavailable", err));
});
