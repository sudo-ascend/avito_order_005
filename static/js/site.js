const DEFAULT_PRICE_LIST_URL = "media/site/prices/price-list.xlsx";
const DEFAULT_PRICE_LIST_DOWNLOAD_NAME = "price-list.xlsx";
const PRICE_LIST_BUTTON_LABEL = "Узнать цены";

const products = [
  {
    image: {
      src: "static/plants_1.webp",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Альтернатера рейнека «Розаэфолия»",
    latin: 'Alternanthera reineckii "Roseafolia"',
    text: "Акцентное красное растение для среднего и заднего плана, добавляет композиции глубину и контраст.",
  },
  {
    image: {
      src: "static/plants_2.webp",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Ротала ротундифолия",
    latin: "Rotala rotundifolia",
    text: "Популярный стебельный вид для ярких групп, мягких переходов и плотных фоновых посадок.",
  },
  {
    image: {
      src: "static/plants_3.webp",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Буцефаландра",
    latin: "Bucephalandra",
    text: "Медленнорастущее растение для коряг и камней, хорошо работает в детальных природных сценах.",
  },
  {
    image: {
      src: "static/plants_4.webp",
      width: 760,
      height: 580,
      position: "center center",
    },
    title: "Анубиас нана",
    latin: "Anubias nana",
    text: "Неприхотливый компактный вид с плотными листьями для переднего плана, коряг и теневых участков.",
  },
  {
    image: {
      src: "static/plants_5.webp",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Криптокорина",
    latin: "Cryptocoryne",
    text: "Розеточное растение для стабильных композиций, хорошо смотрится группами на среднем плане.",
  },
  {
    image: {
      src: "static/plants_6.webp",
      width: 1536,
      height: 1024,
      position: "center center",
    },
    title: "Монте-Карло",
    latin: 'Micranthemum tweediei "Monte Carlo"',
    text: "Почвопокровное растение для плотного зелёного ковра и плавных береговых линий в акваскейпе.",
  },
  {
    image: {
      src: "static/plants_7.webp",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Элеохарис",
    latin: "Eleocharis",
    text: "Тонкая травянистая фактура для переднего плана, полян и естественных переходов между камнями.",
  },
  {
    image: {
      src: "static/plants_8.webp",
      width: 760,
      height: 580,
      position: "center center",
    },
    title: "Людвигия",
    latin: "Ludwigia",
    text: "Выразительное стебельное растение с тёплыми оттенками для цветовых акцентов в композиции.",
  },
];

const resolveImageSource = (image) => image;

const imageMarkup = (image, alt) => {
  const source = resolveImageSource(image);
  const positionStyle = source.position ? ` style="object-position: ${source.position};"` : "";

  return `
    <picture>
      <img src="${source.src}" alt="${alt}" loading="lazy" width="${source.width ?? 760}" height="${source.height ?? 580}"${positionStyle}>
    </picture>
  `;
};

const renderProducts = () => {
  const root = document.querySelector("[data-products]");
  if (!root) return;

  const priceListUrl = root.dataset.priceFileUrl || DEFAULT_PRICE_LIST_URL;
  const priceListDownloadName = root.dataset.priceFileName || DEFAULT_PRICE_LIST_DOWNLOAD_NAME;

  root.innerHTML = products
    .map(
      (product) => `
        <article class="product-card">
          ${imageMarkup(product.image, `${product.title} — аквариумное растение Aquaklon`)}
          <div class="product-card__body">
            <div>
              <h3>${product.title}</h3>
              <em>${product.latin}</em>
            </div>
            <p>${product.text}</p>
            <a class="button button--primary product-card__action" href="${priceListUrl}" download="${priceListDownloadName}">${PRICE_LIST_BUTTON_LABEL}</a>
          </div>
        </article>
      `,
    )
    .join("");
};

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

renderProducts();
initHeader();
initReveal();
initReviewsToggle();
initFlashMessages();
