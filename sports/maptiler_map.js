document.addEventListener("DOMContentLoaded", function () {
    const mapDiv = document.createElement("div");
    mapDiv.id = "map";
    mapDiv.style = "width: 100%; height: 400px; margin-bottom: 15px;";

    const latitudeField = document.getElementById("id_latitude");
    const longitudeField = document.getElementById("id_longitude");
    if (latitudeField && longitudeField) {
        latitudeField.closest(".form-row").insertAdjacentElement("beforebegin", mapDiv);

        const map = new maplibregl.Map({
            container: "map",
            style: "https://api.maptiler.com/maps/streets-v2/?key=slplXG9Cxq6vTARriHni",
            center: [0, 0],
            zoom: 2,
        });

        let marker;
        map.on("click", function (e) {
            const lngLat = e.lngLat;
            const lat = lngLat.lat;
            const lng = lngLat.lng;

            if (marker) {
                marker.setLngLat([lng, lat]);
            } else {
                marker = new maplibregl.Marker().setLngLat([lng, lat]).addTo(map);
            }

            latitudeField.value = lat;
            longitudeField.value = lng;
        });
    }
});
