// Stripe payment form
document.addEventListener("DOMContentLoaded", function () {
  var client_secret = $("#client-secret").val(); // Get client secret
  var stripe = Stripe("pk_test_51Q8npkRo4WFpkduh4hmuGeoGfNevE4C63fyQU0NWkhtO8Zy0JHh78Imm05l1FtpUnaFNachbQiiI4yER1aT1ufL300OBML21aU");
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

  // Create the card element and ensure postal code is shown
  var card = elements.create("card", {
    style: style,
    hidePostalCode: false, // Make sure this is false to show postal code
  });
  card.mount("#card-element");

  // Error handling for the card input
  card.addEventListener("change", function (event) {
    var displayError = document.getElementById("card-errors");
    if (event.error) {
      var html = `
        <span class="icon" role="alert">
          <i class="fas fa-times"></i>
        </span>
        <span>${event.error.message}</span>
      `;
      $(displayError).html(html);
    } else {
      displayError.textContent = "";
    }
  });

  // Handle form submit
  var form = document.getElementById("payment-form");

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();

    var postalCode = document.getElementById("postal-code").value.trim(); // Get postal code

    card.update({ disabled: true });
    $("#submit-button").attr("disabled", true);
    
    // Confirm the payment
    stripe
      .confirmCardPayment(client_secret, {
        payment_method: {
          card: card,
          billing_details: {
            address: {
              postal_code: postalCode, // Include the postal code from the input
            },
          },
        },
      })
      .then(function (result) {
        if (result.error) {
          // Show error message
          var errorDiv = document.getElementById("card-errors");
          var html = `
            <span class="icon" role="alert">
              <i class="fas fa-times"></i>
            </span>
            <span>${result.error.message}</span>`;
          $(errorDiv).html(html);
          card.update({ disabled: false });
          $("#submit-button").attr("disabled", false);
        } else {
          if (result.paymentIntent.status === "succeeded") {
            form.submit(); // Submit the form if payment succeeded
          }
        }
      });
  });
});
