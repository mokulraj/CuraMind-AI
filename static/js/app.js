"use strict";

document.addEventListener(
    "DOMContentLoaded",
    () => {
        initializeNavigation();
        initializeMessages();
        initializePasswordFields();
        initializeFormProtection();
    }
);


function initializeNavigation() {
    const toggle =
        document.querySelector(
            ".navbar-toggle"
        );

    const menu =
        document.querySelector(
            ".navbar-menu"
        );

    if (!toggle || !menu) {
        return;
    }

    toggle.addEventListener(
        "click",
        () => {
            const isOpen =
                menu.classList.toggle(
                    "is-open"
                );

            toggle.setAttribute(
                "aria-expanded",
                String(isOpen)
            );
        }
    );

    const links =
        menu.querySelectorAll(
            "a"
        );

    links.forEach(
        (link) => {
            link.addEventListener(
                "click",
                () => {
                    menu.classList.remove(
                        "is-open"
                    );

                    toggle.setAttribute(
                        "aria-expanded",
                        "false"
                    );
                }
            );
        }
    );

    document.addEventListener(
        "click",
        (event) => {
            if (
                !menu.contains(
                    event.target
                )
                &&
                !toggle.contains(
                    event.target
                )
            ) {
                menu.classList.remove(
                    "is-open"
                );

                toggle.setAttribute(
                    "aria-expanded",
                    "false"
                );
            }
        }
    );
}


function initializeMessages() {
    const closeButtons =
        document.querySelectorAll(
            ".message-close"
        );

    closeButtons.forEach(
        (button) => {
            button.addEventListener(
                "click",
                () => {
                    const message =
                        button.closest(
                            ".message"
                        );

                    if (!message) {
                        return;
                    }

                    message.remove();
                }
            );
        }
    );
}


function initializePasswordFields() {
    const passwordInputs =
        document.querySelectorAll(
            'input[type="password"]'
        );

    passwordInputs.forEach(
        (input) => {
            input.setAttribute(
                "autocomplete",
                input.name
                === "new_password"
                    ? "new-password"
                    : "current-password"
            );
        }
    );
}


function initializeFormProtection() {
    const forms =
        document.querySelectorAll(
            "form"
        );

    forms.forEach(
        (form) => {
            form.addEventListener(
                "submit",
                () => {
                    const submitButton =
                        form.querySelector(
                            'button[type="submit"]'
                        );

                    if (!submitButton) {
                        return;
                    }

                    submitButton.disabled =
                        true;

                    const originalText =
                        submitButton.textContent;

                    submitButton.dataset.originalText =
                        originalText;

                    submitButton.textContent =
                        "Processing...";
                }
            );
        }
    );
}