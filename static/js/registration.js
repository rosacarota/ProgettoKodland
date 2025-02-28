document.addEventListener("DOMContentLoaded", function () {
    let nicknameInput = document.getElementById("nickname");
    let emailInput = document.getElementById("email");
    let passwordInput = document.querySelector("input[name='password']");
    let confirmPasswordInput = document.querySelector("input[name='conferma_password']");
    let nicknameError = document.getElementById("nickname-error");
    let emailError = document.getElementById("email-error");

    let passwordError = document.createElement("small"); // Messaggio di errore per la password
    passwordError.classList.add("text-danger");
    confirmPasswordInput.parentNode.appendChild(passwordError); // Aggiunto sotto il campo password

    let registerForm = document.getElementById("registration-form");
    let submitButton = registerForm.querySelector("button[type='submit']");

    let isUnavailable = false;

    function checkAvailability() {
        let nickname = nicknameInput.value.trim();
        let email = emailInput.value.trim();

        if (nickname === "" && email === "") {
            nicknameError.textContent = "";
            emailError.textContent = "";
            return;
        }

        fetch("/check_nickname_email", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nickname: nickname, email: email })
        })
            .then(response => response.json())
            .then(data => {
                if (data.nickname_esistente) {
                    nicknameError.textContent = "⚠️ Questo nickname è già in uso!";
                    isUnavailable = true;
                } else {
                    nicknameError.textContent = "";
                    isUnavailable = false;
                }

                if (data.email_esistente) {
                    emailError.textContent = "⚠️ Questa email è già registrata!";
                    isUnavailable = true;
                } else {
                    emailError.textContent = "";
                }
                updateSubmitButton();
            });
    }

    function updateSubmitButton() {
        submitButton.disabled = isUnavailable || passwordInput.value !== confirmPasswordInput.value;
    }

    function validateEmail() {
        let emailValue = emailInput.value.trim();
        let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

        if (!emailPattern.test(emailValue) && emailValue !== "") {
            emailError.textContent = "⚠️ Il formato dell'email non è corretto!";
            return false;
        } else {
            emailError.textContent = "";
            return true;
        }
    }

    function validatePasswordMatch() {
        let password = passwordInput.value;
        let confirmPassword = confirmPasswordInput.value;

        if (password !== confirmPassword) {
            passwordError.textContent = "⚠️ Le password non coincidono!";
            confirmPasswordInput.classList.add("is-invalid");
        } else {
            passwordError.textContent = "";
            confirmPasswordInput.classList.remove("is-invalid");
        }
        updateSubmitButton();
    }

    // Aggiungi gli event listener
    nicknameInput.addEventListener("input", checkAvailability);
    emailInput.addEventListener("input", checkAvailability);
    emailInput.addEventListener("blur", validateEmail);
    passwordInput.addEventListener("input", validatePasswordMatch);
    confirmPasswordInput.addEventListener("input", validatePasswordMatch);

    // Controllo finale prima della registrazione
    registerForm.addEventListener("submit", function (event) {
        let isEmailValid = validateEmail();
        let passwordsMatch = passwordInput.value === confirmPasswordInput.value;

        if (!isEmailValid || !passwordsMatch) {
            event.preventDefault();  // Blocca l'invio del modulo se ci sono errori
        }
    });
});
