from django.core.management.base import BaseCommand
from django.db.models import Count
from order.models import CartItem
from store.models import Product


class Command(BaseCommand):
    help = 'ეს ბრძანება გამოიტანს სამ ყველაზე პოპულარულ პროდუქტს.'

    # def add_arguments(self, parser):
    #     # აქ შეგიძლიათ დაამატოთ არგუმენტები, თუ საჭიროა
    #     parser.add_argument('--option', type=str, help='Optional argument')

    def handle(self, *args, **options):
        products = CartItem.objects.values('product_id').annotate(product_count=Count('product_id')).order_by(
                                                                                                '-product_count')[:3]
        product_ids = [obj['product_id'] for obj in products]
        product_names = Product.objects.filter(id__in=product_ids)

        for obj in product_names:
            self.stdout.write(obj.name)
