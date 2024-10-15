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
});
