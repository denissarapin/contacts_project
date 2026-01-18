(function () {
  const phoneDigitsRegex = /^[0-9]+$/;

  function markInvalid(input, message) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    const feedback = input.closest(".mb-3")?.querySelector(".invalid-feedback");
    if (feedback && message) feedback.textContent = message;
  }

  function markValid(input) {
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
  }

  document.addEventListener("submit", function (event) {
    const form = event.target;
    if (!form.classList.contains("needs-validation")) return;

    const emailInput = form.querySelector('input[type="email"]');
    const phoneInput = form.querySelector('input[name="phone_number"]');

    let isOk = true;

    if (emailInput) {
      if (!emailInput.value || !emailInput.checkValidity()) {
        markInvalid(emailInput, "Invalid email address.");
        isOk = false;
      } else {
        markValid(emailInput);
      }
    }

    if (phoneInput) {
      const phoneValue = (phoneInput.value || "").trim();
      
      if (!phoneValue) {
        markInvalid(phoneInput, "Phone number is required.");
        isOk = false;
      } else {
        const digitsOnly = phoneValue.replace(/\D/g, "");
        if (!phoneDigitsRegex.test(digitsOnly)) {
          markInvalid(phoneInput, "Phone number must contain only digits.");
          isOk = false;
        } else if (digitsOnly.length !== 9) {
          markInvalid(phoneInput, "Phone number must be exactly 9 digits.");
          isOk = false;
        } else {
          markValid(phoneInput);
        }
      }
    }

    if (!isOk) {
      event.preventDefault();
      event.stopPropagation();
    }
  }, true);
})();
