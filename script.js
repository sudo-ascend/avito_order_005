const benefits = [
  {
    icon: "shield",
    title: "Чистота посадочного материала",
    text: "Растения выращиваются в стерильной культуре и подходят для аккуратного запуска аквариума.",
  },
  {
    icon: "cup",
    title: "Компактная упаковка",
    text: "Небольшой формат удобно хранить, перевозить и делить на несколько посадочных групп.",
  },
  {
    icon: "tweezers",
    title: "Удобная посадка",
    text: "Порции легко разделяются пинцетом и высаживаются в грунт без лишней массы и мусора.",
  },
  {
    icon: "sprout",
    title: "Хорошая адаптация",
    text: "При правильном свете и питании растения быстро переходят к подводной форме роста.",
  },
  {
    icon: "grid",
    title: "Большой выбор видов",
    text: "Можно подобрать почвопокровные, розеточные, красные и фоновые растения под композицию.",
  },
  {
    icon: "scape",
    title: "Подходит для акваскейпа",
    text: "Чистый старт и ровная посадка помогают создавать плотные природные аквариумные сцены.",
  },
];

const products = [
  {
    image: {
      src: "assets/Alternanthera.png",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Альтернатера рейнека «Розаэфолия»",
    latin: 'Alternanthera reineckii "Roseafolia"',
    text: "Акцентное красное растение для среднего и заднего плана, добавляет композиции глубину и контраст.",
    status: "Уточните наличие и стоимость",
  },
  {
    image: {
      src: "assets/Rotala.png",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Ротала ротундифолия",
    latin: "Rotala rotundifolia",
    text: "Популярный стебельный вид для ярких групп, мягких переходов и плотных фоновых посадок.",
    status: "Цена по запросу",
  },
  {
    image: {
      src: "assets/Bucephalandra.png",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Буцефаландра",
    latin: "Bucephalandra",
    text: "Медленнорастущее растение для коряг и камней, хорошо работает в детальных природных сценах.",
    status: "Наличие уточняйте",
  },
  {
    image: {
      src: "assets/Anubias.webp",
      width: 760,
      height: 580,
      position: "center center",
    },
    title: "Анубиас нана",
    latin: "Anubias nana",
    text: "Неприхотливый компактный вид с плотными листьями для переднего плана, коряг и теневых участков.",
    status: "Цена по запросу",
  },
  {
    image: {
      src: "assets/Cryptocoryne.png",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Криптокорина",
    latin: "Cryptocoryne",
    text: "Розеточное растение для стабильных композиций, хорошо смотрится группами на среднем плане.",
    status: "Наличие уточняйте",
  },
  {
    image: {
      src: "assets/MonteCarlo.png",
      width: 1536,
      height: 1024,
      position: "center center",
    },
    title: "Монте-Карло",
    latin: 'Micranthemum tweediei "Monte Carlo"',
    text: "Почвопокровное растение для плотного зелёного ковра и плавных береговых линий в акваскейпе.",
    status: "Цена по запросу",
  },
  {
    image: {
      src: "assets/Eleocharis.png",
      width: 1122,
      height: 1402,
      position: "center 45%",
    },
    title: "Элеохарис",
    latin: "Eleocharis",
    text: "Тонкая травянистая фактура для переднего плана, полян и естественных переходов между камнями.",
    status: "Уточните наличие и стоимость",
  },
  {
    image: {
      src: "assets/Ludwigia.webp",
      width: 760,
      height: 580,
      position: "center center",
    },
    title: "Людвигия",
    latin: "Ludwigia",
    text: "Выразительное стебельное растение с тёплыми оттенками для цветовых акцентов в композиции.",
    status: "Цена по запросу",
  },
];

const gallery = [
  {
    image: "gallery-aquascape-1",
    title: "Светлая композиция с корягой",
    text: "Живые растения, мягкий свет и естественная линия подводного ландшафта.",
  },
  {
    image: "gallery-aquascape-2",
    title: "Яркий растительный аквариум",
    text: "Стебельные растения создают плотный зелёный фон и ощущение глубины.",
  },
  {
    image: {
      src: "assets/NanoAquascapeStones.png",
      width: 1448,
      height: 1086,
      position: "center center",
    },
    title: "Нано-акваскейп с камнями",
    text: "Компактная композиция, где растения подчёркивают фактуру хардскейпа.",
  },
  {
    image: "gallery-aquascape-4",
    title: "Аккуратный настольный аквариум",
    text: "Минималистичная сцена с живыми растениями и чистой природной формой.",
  },
];

const steps = [
  {
    title: "Вы выбираете растения",
    text: "Ориентируемся на объём аквариума, свет, подачу CO₂ и желаемую композицию.",
  },
  {
    title: "Уточняете наличие",
    text: "Проверяем текущую партию и подбираем близкие варианты, если нужного вида временно нет.",
  },
  {
    title: "Мы консультируем по посадке",
    text: "Подсказываем, как разделить порции, высадить растения и помочь им адаптироваться.",
  },
  {
    title: "Получаете растения для аквариума",
    text: "Компактный посадочный материал готов к запуску, обновлению или плотной досадке.",
  },
];

const reviews = [
  { name: "Алексей В.", rating: 5, text: "Растения пришли свежие, без постороннего запаха. Монте-Карло разделил на маленькие порции, посадка прошла спокойно." },
  { name: "Марина К.", rating: 5, text: "Помогли подобрать виды для небольшого аквариума. Через пару недель всё пошло в рост, особенно ротала." },
  { name: "Дмитрий С.", rating: 5, text: "Понравилась аккуратная упаковка. Баночки компактные, растения чистые, в грунт высаживать удобно." },
  { name: "Елена П.", rating: 4, text: "Брала анубиас и криптокорину. Оба растения адаптировались, лист выглядит плотным и здоровым." },
  { name: "Игорь Н.", rating: 5, text: "Для перезапуска аквариума меристема оказалась удобнее обычных пучков. Меньше мусора и проще контролировать посадку." },
  { name: "Ольга М.", rating: 5, text: "Отдельно спасибо за консультацию по свету. После корректировки режима растения стали выглядеть заметно лучше." },
  { name: "Сергей Т.", rating: 5, text: "Красные растения приехали бодрые. После посадки не растворились, постепенно набирают цвет." },
  { name: "Наталья Р.", rating: 4, text: "Заказ небольшой, но отнеслись внимательно. Всё объяснили по промывке и делению порций." },
  { name: "Павел Г.", rating: 5, text: "Монте-Карло хорошо пошёл ковром. Понравилось, что можно было высадить много маленьких островков." },
  { name: "Анна Л.", rating: 5, text: "Растения выглядели чисто и аккуратно. Для первого акваскейпа формат оказался очень понятным." },
  { name: "Владимир К.", rating: 5, text: "Покупал для среднего плана. Криптокорина прижилась без резких проблем, листья не осыпались." },
  { name: "Кирилл Д.", rating: 4, text: "Наличие уточнили быстро, часть позиций заменили похожими. В аквариуме композиция получилась цельной." },
  { name: "Татьяна Б.", rating: 5, text: "Хорошие компактные растения. Особенно понравилось, что в баночке много материала для рассадки." },
  { name: "Михаил Е.", rating: 5, text: "После посадки растения не всплывали, если делить мелкими пучками. Консультация помогла избежать ошибок." },
  { name: "Юлия С.", rating: 5, text: "Аквариум стал выглядеть свежее и плотнее. Растения без улиток, для меня это было важно." },
  { name: "Роман А.", rating: 5, text: "Заказывал стебельные виды. Пришли аккуратные, цвет хороший, адаптация заняла недолго." },
  { name: "Виктория Н.", rating: 4, text: "Удобно, что можно уточнить наличие перед покупкой. Подобрали растения под мой свет и грунт." },
  { name: "Артём П.", rating: 5, text: "Элеохарис высадил на передний план, выглядит естественно. Баночка была без лишней воды и грязи." },
  { name: "Светлана И.", rating: 5, text: "Очень понравился внешний вид после посадки. Растения небольшие, но их удобно распределить по аквариуму." },
  { name: "Денис Ф.", rating: 5, text: "Брал на запуск нового травника. Старт получился чистый, без случайной живности и старых листьев." },
  { name: "Лариса Ч.", rating: 4, text: "Хорошо объяснили, какие растения лучше для начинающего. Через месяц аквариум выглядит намного гуще." },
  { name: "Константин Р.", rating: 5, text: "Качество стабильно хорошее. Нравится, что растения компактные, а посадочного материала хватает надолго." },
  { name: "Екатерина З.", rating: 5, text: "Получился красивый зелёный передний план. По переписке быстро подсказали, как правильно высадить." },
];

const resolveImageSource = (image) =>
  typeof image === "string"
    ? {
        avif: `assets/${image}.avif`,
        src: `assets/${image}.webp`,
        width: 760,
        height: 580,
      }
    : image;

const imageMarkup = (image, alt, className = "") => {
  const source = resolveImageSource(image);
  const avifSource = source.avif ? `<source srcset="${source.avif}" type="image/avif">` : "";
  const positionStyle = source.position ? ` style="object-position: ${source.position};"` : "";

  return `
    <picture class="${className}">
      ${avifSource}
      <img src="${source.src}" alt="${alt}" loading="lazy" width="${source.width ?? 760}" height="${source.height ?? 580}"${positionStyle}>
    </picture>
  `;
};

const icons = {
  shield: '<svg viewBox="0 0 24 24" focusable="false"><path d="M12 3l7 3v5c0 4.5-2.7 8-7 10-4.3-2-7-5.5-7-10V6l7-3z"/><path d="M8.5 12l2.2 2.2 4.8-5"/></svg>',
  cup: '<svg viewBox="0 0 24 24" focusable="false"><path d="M7 5h10l-1 15H8L7 5z"/><path d="M9 5V3h6v2"/><path d="M8 10h8"/></svg>',
  tweezers: '<svg viewBox="0 0 24 24" focusable="false"><path d="M8 3l4 9-4 9"/><path d="M16 3l-4 9 4 9"/><path d="M10 12h4"/></svg>',
  sprout: '<svg viewBox="0 0 24 24" focusable="false"><path d="M12 21V10"/><path d="M12 10c-4.4 0-7-2.3-8-6 4.5 0 7 2.2 8 6z"/><path d="M12 12c4.2-.2 6.7-2.4 8-6-4.4 0-7 2.1-8 6z"/></svg>',
  grid: '<svg viewBox="0 0 24 24" focusable="false"><path d="M4 4h6v6H4z"/><path d="M14 4h6v6h-6z"/><path d="M4 14h6v6H4z"/><path d="M14 14h6v6h-6z"/></svg>',
  scape: '<svg viewBox="0 0 24 24" focusable="false"><path d="M3 18l5-7 4 5 3-4 6 6"/><path d="M4 20h16"/><path d="M17 5c1.7 0 3 1.3 3 3"/></svg>',
};

const formatReviewName = (name) => name.replace(/^([А-ЯЁа-яё-]+)\s+([А-ЯЁ])\.$/, "$1. $2.");

const renderBenefits = () => {
  const root = document.querySelector("[data-benefits]");
  root.innerHTML = benefits
    .map(
      (item) => `
        <article class="benefit-card">
          <div class="benefit-card__icon" aria-hidden="true">${icons[item.icon]}</div>
          <div>
            <h3>${item.title}</h3>
            <p>${item.text}</p>
          </div>
        </article>
      `,
    )
    .join("");
};

const renderProducts = () => {
  const root = document.querySelector("[data-products]");
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
            <span class="product-card__meta">${product.status}</span>
            <a class="button button--primary" href="#contacts">Уточнить наличие</a>
          </div>
        </article>
      `,
    )
    .join("");
};

const renderGallery = () => {
  const root = document.querySelector("[data-gallery]");
  root.innerHTML = gallery
    .map(
      (item) => `
        <article class="gallery-card">
          ${imageMarkup(item.image, item.title)}
          <div class="gallery-card__caption">
            <h3>${item.title}</h3>
            <p>${item.text}</p>
          </div>
        </article>
      `,
    )
    .join("");
};

const renderSteps = () => {
  const root = document.querySelector("[data-steps]");
  root.innerHTML = steps
    .map(
      (step, index) => `
        <article class="step-card">
          <span>${index + 1}</span>
          <div>
            <h3>${step.title}</h3>
            <p>${step.text}</p>
          </div>
        </article>
      `,
    )
    .join("");
};

let reviewsExpanded = false;

const renderReviews = () => {
  const root = document.querySelector("[data-reviews]");
  const toggle = document.querySelector("[data-reviews-toggle]");
  const visibleReviews = reviewsExpanded ? reviews : reviews.slice(0, 6);

  root.innerHTML = visibleReviews
    .map(
      (review) => `
        <article class="review-card">
          <div class="review-card__stars" aria-label="${review.rating} из 5">${"★".repeat(review.rating)}${"☆".repeat(5 - review.rating)}</div>
          <p>${review.text}</p>
          <strong>${formatReviewName(review.name)}</strong>
        </article>
      `,
    )
    .join("");

  if (toggle) {
    toggle.hidden = reviews.length <= 5;
    toggle.textContent = reviewsExpanded ? "Свернуть отзывы" : "Посмотреть все отзывы";
    toggle.setAttribute("aria-expanded", String(reviewsExpanded));
  }
};

const initReviewsToggle = () => {
  const toggle = document.querySelector("[data-reviews-toggle]");
  if (!toggle) return;

  toggle.addEventListener("click", () => {
    reviewsExpanded = !reviewsExpanded;
    renderReviews();
    if (!reviewsExpanded) {
      document.querySelector("#reviews").scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
};

const initHeader = () => {
  const header = document.querySelector("[data-header]");
  const nav = document.querySelector("[data-nav]");
  const toggle = document.querySelector("[data-nav-toggle]");

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

renderBenefits();
renderProducts();
renderGallery();
renderSteps();
renderReviews();
initReviewsToggle();
initHeader();
initReveal();
