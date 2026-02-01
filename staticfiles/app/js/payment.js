// highlight selected payment option
document.querySelectorAll(".pay-option").forEach(option => {
  option.addEventListener("click", () => {
    // remove active from all
    document.querySelectorAll(".pay-option").forEach(o => o.classList.remove("active"));
    // add active to clicked
    option.classList.add("active");
    option.querySelector("input[type='radio']").checked = true;
  });
});

// form submit handler
document.getElementById("paymentForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const selected = document.querySelector(".pay-option.active input");
    if(!selected){
        alert("Please select a payment method!");
        return;
    }

    const cust = document.querySelector("input[name='custid']:checked");
    if(!cust){
        alert("Please select an address!");
        return;
    }

    if(selected.value === "COD"){
        this.submit(); // normal COD submission
        return;
    }

    // Online payment - Razorpay
    let response = await fetch("/create-payment/", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    });

    let data = await response.json();


    var options = {
        key: data.key,
        amount: data.amount,
        currency: "INR",
        name: "Lucky Store",
        description: "Order Payment",
        order_id: data.order_id,

        handler: function (response) {

            fetch("/razorpay-callback/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    razorpay_payment_id: response.razorpay_payment_id,
                    razorpay_order_id: response.razorpay_order_id,
                    razorpay_signature: response.razorpay_signature,
                    custid: cust.value
                })
            })
            .then(res => res.json())
            .then(result => {
                if(result.status === "success"){
                    window.location.href = "/orders/";
                } else {
                    alert("Payment failed!");
                }
            });
        }
    };

    var rzp1 = new Razorpay(options);
    rzp1.open();
});
