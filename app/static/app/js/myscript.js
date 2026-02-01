/* ===============================
   OWL CAROUSEL (NO CHANGE)
================================ */
$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
});


/* ===============================
   LOGIN – SHOW / HIDE PASSWORD
================================ */
function togglePassword() {
    const passwordField = document.querySelector('input[type="password"]');
    const toggleIcon = document.querySelector('.password-toggle');

    if (!passwordField) return;

    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleIcon.innerHTML = "🙈";
    } else {
        passwordField.type = "password";
        toggleIcon.innerHTML = "";
    }
}

$(document).on('click', '.plus-cart', function (e) {
    let id = $(this).attr("pid");

    $.ajax({
        type: "GET",
        url: "/pluscart/",
        data: {
            prod_id: id
        },
        success: function (data) {
            location.reload(); 
        }
    });
});


$(document).on('click', '.minus-cart', function () {
    let id = $(this).attr("pid");

    $.ajax({
        type: "GET",
        url: "/minuscart/",
        data: {
            prod_id: id
        },
        success: function (data) {
            location.reload();
        }
    });
});


payBtn.onclick = function (e) {
    e.preventDefault();

    if (!selectedMethod) {
        alert("Please select a payment method");
        return;
    }

    if (selectedMethod === "COD") {
        // COD ke liye directly server ko request bhejenge
        fetch("{% url 'cash_on_delivery' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "payment_method": "COD" })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "{% url 'orders' %}";  // Order page redirect
            } else {
                alert("Something went wrong! Try again.");
            }
        });
    } else {
        // Online payment
        rzp1.open();
    }
};
