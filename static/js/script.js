// Stripe payment form
document.addEventListener("DOMContentLoaded", function () {
  var stripe = Stripe(
    "pk_test_51Q8npkRo4WFpkduh4hmuGeoGfNevE4C63fyQU0NWkhtO8Zy0JHh78Imm05l1FtpUnaFNachbQiiI4yER1aT1ufL300OBML21aU"
  );
  var elements = stripe.elements();

  var style = {
    base: {
      fontSize: "16px",
    },
    invalid: {
      color: "#dc3545",
      iconColor: "#dc3545",
    },
  };

  var card = elements.create("card", { style: style });
  card.mount("#card-element");

  // Handle form submission
  document
    .querySelector("#payment-form")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      // This should be the client secret retrieved from the view or stored somewhere else.
      var clientSecret = "client_secret"; // Adjust this line based on your logic.

      stripe
        .confirmCardPayment(clientSecret, {
          payment_method: {
            card: card,
          },
        })
        .then(function (result) {
          if (result.error) {
            // Handle error
            console.error(result.error.message);
          } else {
            // Payment succeeded
            if (result.paymentIntent.status === "succeeded") {
              // Redirect to membership page
              window.location.href = "/membership"; // Redirect to your membership page
            }
          }
        });
    });
});
