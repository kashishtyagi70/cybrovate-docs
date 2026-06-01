// This file keeps small UI behaviors out of the Python backend.
// It handles sidebar collapse, folder expand/collapse, and code copy buttons.

document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const shell = document.querySelector(".app-shell");
    const sidebarToggle = document.querySelector("[data-sidebar-toggle]");
    const mobileSidebarToggle = document.querySelector("[data-mobile-sidebar-toggle]");
    const sidebarOverlay = document.querySelector("[data-sidebar-overlay]");
    const themeToggle = document.querySelector("[data-theme-toggle]");
    const desktopSidebarQuery = window.matchMedia("(min-width: 861px)");

    // Updates the topbar theme button and stores the selected theme.
    const setTheme = (theme, shouldSave = false) => {
        const nextTheme = theme === "light" ? "light" : "dark";

        root.setAttribute("data-theme", nextTheme);
        document.body?.setAttribute("data-theme", nextTheme);

        if (shouldSave) {
            try {
                localStorage.setItem("cybrovateTheme", nextTheme);
            } catch (error) {
                // Theme still changes even if browser storage is blocked.
            }
        }

        if (themeToggle) {
            const nextLabel = nextTheme === "light" ? "Switch to dark theme" : "Switch to light theme";

            themeToggle.setAttribute("aria-label", nextLabel);
            themeToggle.setAttribute("aria-pressed", String(nextTheme === "light"));
            themeToggle.setAttribute("title", nextLabel);
        }
    };

    // Keep the button label correct for the theme set in base.html.
    setTheme(root.getAttribute("data-theme") || "dark");

    // The topbar circle button toggles between dark and light mode.
    themeToggle?.addEventListener("click", () => {
        const currentTheme = root.getAttribute("data-theme") === "light" ? "light" : "dark";
        setTheme(currentTheme === "light" ? "dark" : "light", true);
    });

    // Saves the desktop sidebar state so refreshes keep the user's preference.
    const setDesktopSidebarCollapsed = (collapsed) => {
        if (!shell || !sidebarToggle) {
            return;
        }

        shell.classList.toggle("sidebar-collapsed", collapsed);
        sidebarToggle.setAttribute("aria-expanded", String(!collapsed));
        sidebarToggle.setAttribute("aria-label", collapsed ? "Expand sidebar" : "Collapse sidebar");

        try {
            localStorage.setItem("cybrovateSidebarCollapsed", String(collapsed));
        } catch (error) {
            // The sidebar still collapses even if browser storage is blocked.
        }
    };

    // Mobile sidebar opens like a drawer, independent from the desktop collapse state.
    const setMobileSidebarOpen = (open) => {
        if (!shell || !mobileSidebarToggle) {
            return;
        }

        shell.classList.toggle("sidebar-mobile-open", open);
        document.body.classList.toggle("sidebar-lock", open);
        mobileSidebarToggle.setAttribute("aria-expanded", String(open));
        mobileSidebarToggle.setAttribute("aria-label", open ? "Close documentation navigation" : "Open documentation navigation");
    };

    // Restore desktop collapsed state after page reload.
    if (shell && sidebarToggle) {
        try {
            if (localStorage.getItem("cybrovateSidebarCollapsed") === "true") {
                setDesktopSidebarCollapsed(true);
            }
        } catch (error) {
            // Ignore blocked storage and keep the sidebar expanded by default.
        }
    }

    // The sidebar collapse button is shown inside the sidebar on desktop.
    sidebarToggle?.addEventListener("click", () => {
        if (!desktopSidebarQuery.matches) {
            return;
        }

        setDesktopSidebarCollapsed(!shell.classList.contains("sidebar-collapsed"));
    });

    // The topbar menu button opens navigation on mobile.
    mobileSidebarToggle?.addEventListener("click", () => {
        setMobileSidebarOpen(!shell.classList.contains("sidebar-mobile-open"));
    });

    // Tapping the backdrop closes mobile navigation.
    sidebarOverlay?.addEventListener("click", () => {
        setMobileSidebarOpen(false);
    });

    // Close the mobile drawer after selecting a page link.
    document.querySelectorAll(".navigation a").forEach((link) => {
        link.addEventListener("click", () => {
            setMobileSidebarOpen(false);
        });
    });

    // Each sidebar folder can be expanded or collapsed.
    document.querySelectorAll("[data-nav-section-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const section = button.closest(".nav-section");

            if (!section) {
                return;
            }

            const nextCollapsed = !section.classList.contains("is-collapsed");
            section.classList.toggle("is-collapsed", nextCollapsed);
            button.setAttribute("aria-expanded", String(!nextCollapsed));
        });
    });

    // Tries modern clipboard first, then falls back to the older textarea copy path.
    const writeTextToClipboard = async (text) => {
        if (window.navigator?.clipboard?.writeText) {
            try {
                await window.navigator.clipboard.writeText(text);
                return true;
            } catch (error) {
                // Some browser contexts block the modern clipboard API.
            }
        }

        const textarea = document.createElement("textarea");

        textarea.value = text;
        textarea.setAttribute("readonly", "");
        textarea.style.position = "fixed";
        textarea.style.top = "-1000px";
        textarea.style.left = "-1000px";
        document.body.appendChild(textarea);
        textarea.select();

        const copied = document.execCommand?.("copy") || false;
        textarea.remove();
        return copied;
    };

    // Adds a copy button to every fenced markdown code block.
    document.querySelectorAll(".document pre").forEach((pre) => {
        if (pre.closest(".code-block")) {
            return;
        }

        const code = pre.querySelector("code");
        const wrapper = document.createElement("div");
        const copyButton = document.createElement("button");

        wrapper.className = "code-block";
        copyButton.type = "button";
        copyButton.className = "copy-code-button";
        copyButton.textContent = "Copy";
        copyButton.setAttribute("aria-label", "Copy code block");

        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);
        wrapper.appendChild(copyButton);

        copyButton.addEventListener("click", async () => {
            const text = code ? code.innerText : pre.innerText;

            if (await writeTextToClipboard(text)) {
                copyButton.textContent = "Copied";
                window.setTimeout(() => {
                    copyButton.textContent = "Copy";
                }, 1400);
            } else {
                // Last fallback: select the code text so the user can copy manually.
                const selection = window.getSelection();
                const range = document.createRange();

                range.selectNodeContents(code || pre);
                selection?.removeAllRanges();
                selection?.addRange(range);
                copyButton.textContent = "Select";
            }
        });
    });

    // Preserve scroll position for each markdown page when navigating back/forward.
    const docsContent = document.querySelector(".content");

    if (docsContent) {
        const scrollStorageKey = `cybrovateDocsScroll:${window.location.pathname}`;
        let scrollSaveTimer;

        if ("scrollRestoration" in window.history) {
            window.history.scrollRestoration = "manual";
        }

        const saveScrollPosition = () => {
            try {
                sessionStorage.setItem(
                    scrollStorageKey,
                    JSON.stringify({
                        contentTop: docsContent.scrollTop,
                        windowTop: window.scrollY,
                    })
                );
            } catch (error) {
                // Navigation still works normally if browser storage is blocked.
            }
        };

        const restoreScrollPosition = () => {
            if (window.location.hash) {
                return;
            }

            try {
                const savedPosition = JSON.parse(sessionStorage.getItem(scrollStorageKey) || "{}");

                if (Number.isFinite(savedPosition.contentTop)) {
                    docsContent.scrollTop = savedPosition.contentTop;
                }

                if (Number.isFinite(savedPosition.windowTop)) {
                    window.scrollTo(0, savedPosition.windowTop);
                }
            } catch (error) {
                // Ignore invalid saved data and leave the page at the browser default.
            }
        };

        docsContent.addEventListener(
            "scroll",
            () => {
                window.clearTimeout(scrollSaveTimer);
                scrollSaveTimer = window.setTimeout(saveScrollPosition, 80);
            },
            { passive: true }
        );

        window.addEventListener(
            "scroll",
            () => {
                window.clearTimeout(scrollSaveTimer);
                scrollSaveTimer = window.setTimeout(saveScrollPosition, 80);
            },
            { passive: true }
        );

        window.addEventListener("pagehide", saveScrollPosition);
        document.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "hidden") {
                saveScrollPosition();
            }
        });

        requestAnimationFrame(() => {
            restoreScrollPosition();
            window.setTimeout(restoreScrollPosition, 150);
        });
    }
});
