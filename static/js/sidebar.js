"use strict";


document.addEventListener(
    "DOMContentLoaded",
    () => {

        const menuButton =
            document.getElementById(
                "mobile-menu-button"
            );


        const sidebar =
            document.getElementById(
                "sidebar"
            );


        if (!menuButton || !sidebar) {
            return;
        }


        menuButton.addEventListener(
            "click",
            () => {

                const isOpen =
                    sidebar.classList.toggle(
                        "open"
                    );


                menuButton.setAttribute(
                    "aria-expanded",
                    String(isOpen)
                );

            }
        );


        document.addEventListener(
            "click",
            (event) => {

                if (
                    window.innerWidth > 900
                ) {
                    return;
                }


                const clickedInsideSidebar =
                    sidebar.contains(
                        event.target
                    );


                const clickedMenuButton =
                    menuButton.contains(
                        event.target
                    );


                if (
                    !clickedInsideSidebar &&
                    !clickedMenuButton
                ) {

                    sidebar.classList.remove(
                        "open"
                    );


                    menuButton.setAttribute(
                        "aria-expanded",
                        "false"
                    );

                }

            }
        );

    }
);