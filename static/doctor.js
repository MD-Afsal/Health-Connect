$(document).ready(function() {
    function fetchDoctorDetails(category) {
        $.ajax({
            url: '/get_doctor_details', 
            method: 'GET',
            data: { category: category },
            success: function(response) {
                
                $('.doctor-details').html(response);
            },
            error: function(xhr, status, error) {
                console.error('Error fetching doctor details:', error);
            }
        });
    }


    $('.dropdown-content a').click(function(event) {
        event.preventDefault();
        var category = $(this).text().trim();
        fetchDoctorDetails(category);
    });

});

$(document).ready(function() {

    function fetchCardDetails(phone_no, name) {
        $.ajax({
            url:'/get_card_details',
            method:'GET', // Corrected the spelling of 'method'
            data: {phone_no: phone_no.value, name: name.value}, // Get the values of the DOM elements
            success: function(response) {
                $('.card-details').html(response);
            },
            error: function(xhr, status, error){
                console.error('Error on fetching the card details:', error);
            }
        });
    }

    $('.doctor-card').click(function(event) {
        event.preventDefault();
      
        // var phone_no = $(this).text();  // Adjust selector for phone element
        // var name = $(this).text();    // Adjust selector for name element
      
        fetchCardDetails(phone_no, name);
      });

});

