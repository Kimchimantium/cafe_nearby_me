// Define initMap in the global scope
function initMap() {
    console.log('initMap function called.');
    // Assuming mapKey and locationName are globally accessible
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': locationName }, function(results, status) {
        if (status == 'OK') {
            const mapOptions = {
                zoom: 15,
                center: results[0].geometry.location
            };
            const map = new google.maps.Map(document.getElementById("map"), mapOptions);
            new google.maps.Marker({
                position: results[0].geometry.location,
                map: map
            });
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOMContentLoaded event fired.');
    // Ensure mapKey and locationName are defined and accessible here
});

// Dynamically load the Google Maps script
function loadGoogleMapsScript() {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${mapKey}&callback=initMap`;
    script.async = true;
    document.head.appendChild(script);
}

// Call loadGoogleMapsScript after ensuring initMap is defined
loadGoogleMapsScript();
