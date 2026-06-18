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

initHeader();
initReveal();
initReviewsToggle();
initFlashMessages();
