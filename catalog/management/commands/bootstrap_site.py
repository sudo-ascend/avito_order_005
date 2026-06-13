from django.core.management.base import BaseCommand

from catalog.models import Benefit, GalleryItem, OrderStep, Review, SiteConfiguration


class Command(BaseCommand):
    help = "Заполняет сайт стартовым контентом."

    def handle(self, *args, **options):
        SiteConfiguration.objects.get_or_create(pk=1)

        if not Benefit.objects.exists():
            Benefit.objects.bulk_create(
                [
                    Benefit(sort_order=1, icon="shield", title="Чистый посадочный материал", text="Растения выращиваются в стерильной культуре и подходят для аккуратного запуска аквариума."),
                    Benefit(sort_order=2, icon="cup", title="Компактная упаковка", text="Небольшой формат удобно хранить, перевозить и делить на несколько посадочных групп."),
                    Benefit(sort_order=3, icon="tweezers", title="Удобная посадка", text="Порции легко разделяются пинцетом и высаживаются без лишней массы и мусора."),
                    Benefit(sort_order=4, icon="sprout", title="Быстрая адаптация", text="При правильном свете и питании растения спокойно переходят к подводной форме роста."),
                    Benefit(sort_order=5, icon="grid", title="Большой выбор видов", text="Можно подобрать почвопокровные, розеточные, красные и фоновые растения под композицию."),
                    Benefit(sort_order=6, icon="scape", title="Подходит для акваскейпа", text="Чистый старт и ровная посадка помогают создавать плотные природные сцены."),
                ]
            )

        if not GalleryItem.objects.exists():
            GalleryItem.objects.bulk_create(
                [
                    GalleryItem(sort_order=1, title="Светлая композиция с корягой", text="Живые растения, мягкий свет и естественная линия подводного ландшафта.", image_path="gallery-aquascape-1.webp"),
                    GalleryItem(sort_order=2, title="Яркий растительный аквариум", text="Стебельные растения создают плотный зеленый фон и ощущение глубины.", image_path="gallery-aquascape-2.webp"),
                    GalleryItem(sort_order=3, title="Нано-акваскейп с камнями", text="Компактная композиция, где растения подчеркивают фактуру хардскейпа.", image_path="NanoAquascapeStones.png"),
                    GalleryItem(sort_order=4, title="Аккуратный настольный аквариум", text="Минималистичная сцена с живыми растениями и чистой природной формой.", image_path="gallery-aquascape-4.webp"),
                ]
            )

        if not OrderStep.objects.exists():
            OrderStep.objects.bulk_create(
                [
                    OrderStep(sort_order=1, title="Вы выбираете растения", text="Ориентируемся на объем аквариума, свет, подачу CO2 и желаемую композицию."),
                    OrderStep(sort_order=2, title="Уточняете наличие", text="Проверяем текущую партию и предлагаем близкие варианты, если нужного вида временно нет."),
                    OrderStep(sort_order=3, title="Получаете рекомендации по посадке", text="Подсказываем, как разделить порции и помочь растениям адаптироваться."),
                    OrderStep(sort_order=4, title="Высаживаете в аквариум", text="Компактный посадочный материал подходит для запуска, обновления или плотной досадки."),
                ]
            )

        if not Review.objects.exists():
            Review.objects.bulk_create(
                [
                    Review(sort_order=1, name="Алексей В.", rating=5, text="Растения пришли свежие, без постороннего запаха. Посадка прошла спокойно."),
                    Review(sort_order=2, name="Марина К.", rating=5, text="Помогли подобрать виды для небольшого аквариума. Через пару недель все пошло в рост."),
                    Review(sort_order=3, name="Дмитрий С.", rating=5, text="Аккуратная упаковка и чистые баночки. Высаживать в грунт было удобно."),
                    Review(sort_order=4, name="Елена П.", rating=4, text="Анубиас и криптокорина адаптировались без проблем, лист выглядит плотным и здоровым."),
                    Review(sort_order=5, name="Игорь Н.", rating=5, text="Для перезапуска аквариума меристема оказалась удобнее обычных пучков."),
                    Review(sort_order=6, name="Ольга М.", rating=5, text="Отдельное спасибо за консультацию по свету. После корректировки режима растения стали выглядеть лучше."),
                ]
            )

        self.stdout.write(self.style.SUCCESS("Стартовый контент готов."))
