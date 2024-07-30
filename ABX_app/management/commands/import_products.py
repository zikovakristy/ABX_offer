import csv
from django.core.management.base import BaseCommand
from ABX_app.models import Product, ProductType

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Ensure product_type exists
                product_type_id = row['product_type_id']
                try:
                    product_type = ProductType.objects.get(id=product_type_id)
                except ProductType.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'ProductType ID "{product_type_id}" does not exist.'))
                    continue

                # Create product
                Product.objects.create(
                    item_code=row['item_code'],
                    name=row['name'],
                    description=row['description'],
                    url=row['url'],
                    sale_price=row['sale_price'],
                    purchase_price=row['purchase_price'],
                    default=row['default'] == 'True',
                    product_type=product_type,
                    HS=row['HS'] == 'True',
                    AS=row['AS'] == 'True',
                    RC=row['RC'] == 'True',
                    PC=row['PC'] == 'True',
                    sleva=row['sleva'] == 'True',
                    DPH=row['DPH']
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported products'))
