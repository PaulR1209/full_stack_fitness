// Stripe payment form (not needed if using Stripe Checkout)
document.addEventListener("DOMContentLoaded", () => {
  const clientSecret = $("#client-secret").val();
  const stripe = Stripe(
    "pk_test_51Q8npkRo4WFpkduh4hmuGeoGfNevE4C63fyQU0NWkhtO8Zy0JHh78Imm05l1FtpUnaFNachbQiiI4yER1aT1ufL300OBML21aU"
  );

  const form = $("#payment-form");

  // Handle form submission
  form.on("submit", (ev) => {
    ev.preventDefault();

    // Redirect to Stripe Checkout
    stripe
      .redirectToCheckout({
        sessionId: clientSecret, // Assuming you get the session ID from your backend
      })
      .then((result) => {
        // Handle any errors that occur during redirection
        if (result.error) {
          console.error(result.error.message); // Log the error for debugging
        }
      });
  });
});
