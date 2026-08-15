"use strict";


document.addEventListener(
    "DOMContentLoaded",
    () => {

        initializeMobileNavigation();

        initializeSidebarLinks();

    }
);


function initializeMobileNavigation() {

    const menuButton =
        document.querySelector(
            ".mobile-menu-button"
        );

    const sidebar =
        document.querySelector(
            ".sidebar"
        );

    const overlay =
        document.querySelector(
            ".mobile-sidebar-overlay"
        );

    const moreButton =
        document.querySelector(
            ".mobile-more-button"
        );


    if (!sidebar) {
        return;
    }


    function openMenu() {

        sidebar.classList.add(
            "is-open"
        );


        if (overlay) {

            overlay.classList.add(
                "is-visible"
            );

            overlay.setAttribute(
                "aria-hidden",
                "false"
            );

        }


        document.body.classList.add(
            "mobile-menu-open"
        );


        if (menuButton) {

            menuButton.setAttribute(
                "aria-expanded",
                "true"
            );

        }

    }


    function closeMenu() {

        sidebar.classList.remove(
            "is-open"
        );


        if (overlay) {

            overlay.classList.remove(
                "is-visible"
            );

            overlay.setAttribute(
                "aria-hidden",
                "true"
            );

        }


        document.body.classList.remove(
            "mobile-menu-open"
        );


        if (menuButton) {

            menuButton.setAttribute(
                "aria-expanded",
                "false"
            );

        }

    }


    if (menuButton) {

        menuButton.addEventListener(
            "click",
            () => {

                if (
                    sidebar.classList.contains(
                        "is-open"
                    )
                ) {

                    closeMenu();

                } else {

                    openMenu();

                }

            }
        );

    }


    if (moreButton) {

        moreButton.addEventListener(
            "click",
            openMenu
        );

    }


    if (overlay) {

        overlay.addEventListener(
            "click",
            closeMenu
        );

    }


    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Escape"
            ) {

                closeMenu();

            }

        }
    );


    window.addEventListener(
        "resize",
        () => {

            if (
                window.innerWidth > 768
            ) {

                closeMenu();

            }

        }
    );


    document
        .querySelectorAll(
            ".sidebar-link"
        )
        .forEach(
            (link) => {

                link.addEventListener(
                    "click",
                    () => {

                        if (
                            window.innerWidth <= 768
                        ) {

                            closeMenu();

                        }

                    }
                );

            }
        );

}


function initializeSidebarLinks() {

    const links =
        document.querySelectorAll(
            ".sidebar-link"
        );


    links.forEach(
        (link) => {

            link.addEventListener(
                "click",
                () => {

                    links.forEach(
                        (item) => {

                            item.classList.remove(
                                "active"
                            );

                        }
                    );


                    link.classList.add(
                        "active"
                    );

                }
            );

        }
    );

}