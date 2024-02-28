let map; // Global map variable
let lastMarker; // Global marker variable to keep track of the last marker

// Define initMap in the global scope
function initMap() {
    console.log('initMap function called.');
    // Initialize a default map here instead of inside the geocode callback
    const mapOptions = {
        zoom: 15,
        center: new google.maps.LatLng(37.3588478, 127.1051678) //
    };
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
}

// Dynamically load the Google Maps script
function loadGoogleMapsScript() {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${mapKey}&callback=initMap`;
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
        const rowInfo = JSON.parse(rowData);

        // send this information to your Flask app
        fetch('/', { // Ensure the endpoint is correct
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
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, rating, vicinity }),
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error('Error:', error));

            // Optionally, update the UI to reflect the change
        });
    });
});
//edit form collapse mycafes.html
document.addEventListener('DOMContentLoaded', function () {
    var myCollapseElements = document.querySelectorAll('.collapse');
    myCollapseElements.forEach(function(elem) {
        elem.addEventListener('show.bs.collapse', function () {
            myCollapseElements.forEach(function(otherElem) {
                if (elem !== otherElem && otherElem.classList.contains('show')) {
                    var collapseInstance = new bootstrap.Collapse(otherElem, {
                        toggle: false
                    });
                    collapseInstance.hide();
                }
            });
        });
    });
});
function submitForm(event, cafeId) {
    event.preventDefault(); // Prevent the default form submission
    var form = document.getElementById('form-' + cafeId);
    var formData = new FormData(form);

    fetch('/submit', { // Ensure this URL matches your Flask route
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        // Collapse the form here or show a success message
        $('#collapseEdit-' + cafeId).collapse('hide');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
$(document).ready(function(){
    // Listen for click events on elements with the class 'add-cafe'
    $('.add-cafe').click(function(e){
        e.preventDefault(); // Prevent the default action

        // Change the class of the <i> child element to switch icons
        $(this).find('i').removeClass('fa-plus').addClass('fa-flag');

        // Optionally, you can also change the anchor class for styling or to prevent re-clicks
        $(this).removeClass('add-cafe').addClass('cafe-added');

        // Additional logic for sending data to the server or updating the UI
    });
    $('.add-favorite').click(function(e){
    e.preventDefault(); // Prevent the default action

    var $this = $(this); // Cache this for use in AJAX callback

    // Extract cafe_id and action from the anchor's href attribute
    var url = $this.attr('href');

    // Perform an AJAX request to the server
    $.ajax({
        url: url,
        type: 'GET', // Or 'POST', depending on how your server expects to receive the request
        success: function(response) {
            // Assuming the server sends back a success response
            // Now update the UI to reflect the change

            // Change the class of the <i> child element to switch icons
            $this.find('i').removeClass('fa-regular').addClass('fa-solid');

            // Optionally, you can also change the anchor class for styling or to prevent re-clicks
            $this.removeClass('add-favorite').addClass('favorite');

            // You can also update other parts of your UI based on the response
            // For example, showing a message to the user
            // $('#success-message').text('Cafe added to favorites!').show();
        },
        error: function(xhr, status, error) {
            // Handle any errors here
            console.error("An error occurred: " + error);
            // Optionally, display an error message to the user
            // $('#error-message').text('Failed to add cafe to favorites. Please try again.').show();
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var collapseElement = document.getElementById('collapseExample');
    var toggleButton = document.getElementById('toggleListButton');

    // Listen for the collapse to finish opening
    collapseElement.addEventListener('show.bs.collapse', function () {
        toggleButton.textContent = 'Hide List'; // Change button text
    });

    // Listen for the collapse to finish closing
    collapseElement.addEventListener('hide.bs.collapse', function () {
        toggleButton.textContent = 'Show List'; // Change button text
    });
});