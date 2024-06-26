$(document).ready(function () {
    function fetchDoctorDetails(category) {
        $.ajax({
            url: '/get_doctor_details',
            method: 'GET',
            data: { category: category },
            success: function (response) {

                $('.doctor-details').html(response);
            },
            error: function (xhr, status, error) {
                console.error('Error fetching doctor details:', error);
            }
        });
    }

    $('.dropdown-content a').click(function (event) {
        event.preventDefault();
        var category = $(this).text().trim();
        fetchDoctorDetails(category);
    });

});

$(document).ready(function () {

    $(document).on('click', '.doctor-card', function(event) {
        event.preventDefault();
        var phone_no = $(this).find("#phone_number").text().replace(/\D/g, '');
        console.log(phone_no)
        fetchCardDetails(phone_no);
    });

    function fetchCardDetails(phone_no) {
        $.ajax({
            url: '/get_card_details',
            method: 'GET',
            data: { phone_no: phone_no },
            success: function (response) {
                var newWindow = window.open();
                newWindow.document.write(response);
            },
            error: function (xhr, status, error) {
                console.error('Error on fetching the card details:', error);
            }
        });
    }
});

