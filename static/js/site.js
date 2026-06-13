const initHeader = () => {
  const header = document.querySelector("[data-header]");
  const nav = document.querySelector("[data-nav]");
  const toggle = document.querySelector("[data-nav-toggle]");
  if (!header || !nav || !toggle) return;

  const syncScroll = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  };

  const closeNav = () => {
    document.body.classList.remove("nav-open");
    nav.classList.remove("is-open");
    header.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Открыть меню");
  };

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("is-open");
    header.classList.toggle("is-open", isOpen);
    document.body.classList.toggle("nav-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
    toggle.setAttribute("aria-label", isOpen ? "Закрыть меню" : "Открыть меню");
  });

  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeNav();
  });

  window.addEventListener("scroll", syncScroll, { passive: true });
  syncScroll();
};

const initReveal = () => {
  const sections = document.querySelectorAll(".section-observe");
  if (!sections.length || typeof IntersectionObserver === "undefined") return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.14 },
  );

  sections.forEach((section) => observer.observe(section));
};

const initReviewsToggle = () => {
  const toggle = document.querySelector("[data-reviews-toggle]");
  if (!toggle) return;

  const hiddenReviews = document.querySelectorAll(".is-hidden-review");
  let expanded = false;

  const renderState = () => {
    hiddenReviews.forEach((item) => item.classList.toggle("review-visible", expanded));
    toggle.textContent = expanded ? toggle.dataset.hideText : toggle.dataset.showText;
    toggle.setAttribute("aria-expanded", String(expanded));
  };

  toggle.addEventListener("click", () => {
    expanded = !expanded;
    renderState();
    if (!expanded) {
      document.querySelector("#reviews")?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  renderState();
};

const initFlashMessages = () => {
  const stack = document.querySelector("[data-flash-stack]");
  const flashes = document.querySelectorAll("[data-flash]");
  if (!flashes.length) return;

  flashes.forEach((flash) => {
    const bar = flash.querySelector("[data-flash-bar]");

    window.requestAnimationFrame(() => {
      bar?.classList.add("is-animating");
    });

    window.setTimeout(() => {
      flash.classList.add("is-hiding");
      window.setTimeout(() => {
        flash.remove();
        if (stack && !stack.querySelector("[data-flash]")) {
          stack.remove();
        }
      }, 400);
    }, 3000);
  });
};

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
  return "";
};

const initFavorites = () => {
  const buttons = document.querySelectorAll("[data-favorite-toggle]");
  if (!buttons.length) return;

  const csrfToken = getCookie("csrftoken");
  const countNodes = document.querySelectorAll("[data-favorite-count]");
  const favoritesPage = document.querySelector("[data-favorites-page]");
  const favoritesGrid = document.querySelector("[data-favorites-grid]");
  const emptyNodes = document.querySelectorAll("[data-favorites-empty]");

  const syncButtonState = (button, isFavorite) => {
    button.classList.toggle("is-active", isFavorite);
    button.setAttribute("aria-pressed", String(isFavorite));
    button.setAttribute("aria-label", isFavorite ? "Убрать из избранного" : "Добавить в избранное");
  };

  const syncFavoriteCount = (count) => {
    countNodes.forEach((node) => {
      node.textContent = String(count);
    });
  };

  const syncFavoritesPageState = () => {
    if (!favoritesPage || !favoritesGrid) return;
    const hasCards = Boolean(favoritesGrid.querySelector("[data-product-card]"));
    favoritesGrid.classList.toggle("is-hidden", !hasCards);
    emptyNodes.forEach((node) => {
      node.classList.toggle("is-hidden", hasCards);
    });
  };

  buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      if (button.disabled) return;

      button.disabled = true;
      try {
        const response = await fetch(button.dataset.toggleUrl, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
        });

        if (!response.ok) {
          throw new Error("Favorite toggle failed");
        }

        const payload = await response.json();
        syncButtonState(button, payload.is_favorite);
        syncFavoriteCount(payload.favorite_count);

        if (favoritesPage && !payload.is_favorite) {
          button.closest("[data-product-card]")?.remove();
          syncFavoritesPageState();
        }
      } catch (_error) {
        button.classList.add("is-error");
        window.setTimeout(() => button.classList.remove("is-error"), 900);
      } finally {
        button.disabled = false;
      }
    });
  });

  syncFavoritesPageState();
};

initHeader();
initReveal();
initReviewsToggle();
initFlashMessages();
initFavorites();
