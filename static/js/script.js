// Stripe payment form
document.addEventListener("DOMContentLoaded", function () {
  var client_secret = $("#client-secret").val();
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

  var card = elements.create("card", {
    style: style,
    hidePostalCode: false,
  });
  card.mount("#card-element");

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

  var form = document.getElementById("payment-form");

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();

    var postalCode = document.getElementById("postal-code").value.trim();

    card.update({ disabled: true });
    $("#submit-button").attr("disabled", true);
    
    stripe
      .confirmCardPayment(client_secret, {
        payment_method: {
          card: card,
          billing_details: {
            address: {
              postal_code: postalCode,
            },
          },
        },
      })
      .then(function (result) {
        if (result.error) {
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
            form.submit();
          }
        }
      });
  });
});
