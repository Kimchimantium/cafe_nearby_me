let map; // Global map variable
let lastMarker; // Global marker variable to keep track of the last marker

// Define initMap in the global scope
function initMap() {
    console.log('initMap function called.');
    // Initialize a default map here instead of inside the geocode callback
    const mapOptions = {
        zoom: 14,
        center: new google.maps.LatLng(37.5758772, 126.9768121) // Default center, e.g., Sydney
    };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}

// Dynamically load the Google Maps script
function loadGoogleMapsScript() {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${mapKey}&callback=initMap`; // Ensure mapKey is defined
    script.async = true;
    document.head.appendChild(script);
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOMContentLoaded event fired.');
    loadGoogleMapsScript();
    setupLocationListeners(); // Set up location listeners
});

function setupLocationListeners() {
    // Listen for clicks on elements with the class 'font-weight-bold' and the 'data-location' attribute
    document.addEventListener('click', function(e) {
        // Check if the clicked element matches the criteria
        if (e.target && e.target.matches('.font-weight-bold[data-location]')) {
            e.preventDefault(); // Prevent the default action, if any

            const locationName = e.target.getAttribute('data-location');

            // Use the geocoder to find the location and update the map
            const geocoder = new google.maps.Geocoder();
            geocoder.geocode({ 'address': locationName }, function(results, status) {
                if (status === 'OK') {
                    if (lastMarker) {
                        lastMarker.setMap(null); // Remove the last marker from the map
                    }
                    map.setCenter(results[0].geometry.location);
                    lastMarker = new google.maps.Marker({
                        position: results[0].geometry.location,
                        map: map
                    });
                } else {
                    console.error('Geocode was not successful for the following reason: ' + status);
                }
            });
        }
    });
}

document.querySelectorAll('.icon-plus').forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent the default anchor action

        const rowData = this.getAttribute('data-row-info');
        const rowInfo = JSON.parse(rowData); // Ensure this is properly formatted JSON

        // Now, send this information to your Flask app
        fetch('/your-flask-endpoint', { // Ensure the endpoint is correct
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(rowInfo),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle any response here
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.add-cafe').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent the link from navigating to a new URL
            const name = this.getAttribute('data-name');
            const rating = this.getAttribute('data-rating');
            const vicinity = this.getAttribute('data-vicinity');

            // Send the data to the server using Fetch API
            fetch('/', {
                method: 'POST', // or 'GET' if you're appending data to the URL
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, rating, vicinity }),
                // If you're using GET, you might not send a body but append data to the URL
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));

            // Optionally, update the UI to reflect the change
        });
    });
});