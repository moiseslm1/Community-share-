const mapContainer = document.getElementById("map");

if (mapContainer) {

    mapboxgl.accessToken = "YOUR_MAPBOX_TOKEN";

    const map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v12",
        center: [-118.2437, 34.0522],
        zoom: 10
    });

    const services = [
        { name: "Dog Walking", coords: [-118.25, 34.05] },
        { name: "Cleaning", coords: [-118.28, 34.06] }
    ];

    services.forEach(service => {
        new mapboxgl.Marker()
            .setLngLat(service.coords)
            .setPopup(new mapboxgl.Popup().setText(service.name))
            .addTo(map);
    });

}