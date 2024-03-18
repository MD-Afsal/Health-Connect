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
