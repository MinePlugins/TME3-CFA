from django.core.management.base import BaseCommand, CommandError
from myStockProduct.models import ProductStock
from myStockProduct.serializers import ProductStockSerializer
from mytig.models import ProduitEnPromotion
from mytig.serializers import ProduitEnPromotionSerializer
from mytig.config import baseUrl
import requests
import time
from random import randrange


class Command(BaseCommand):
    help = 'Refresh the list of products which are on sale.'

    def handle(self, *args, **options):
        self.stdout.write('['+time.ctime()+'] Refreshing data...')
        response = requests.get(baseUrl+'products/')
        jsondata = response.json()
        for product in jsondata:
            prod = None
            try:
                prod = ProductStock.objects.get(tigID=product['id'])
            except ProductStock.DoesNotExist:
                prod = None

            if prod is not None:
                if prod.quantityInStock > 16 and prod.quantityInStock < 64:
                    before_diff = product['price'] * 0.80
                    after_diff = abs(before_diff-product['price'])
                elif prod.quantityInStock >= 64:
                    before_diff = product['price'] * 0.50
                    after_diff = abs(before_diff-product['price'])
                else:
                    after_diff = 0
                prodstock = None
                try:
                    prodstock = ProduitEnPromotion.objects.get(tigID=product['id'])
                except:
                    prodstock = None
                if prodstock is not None:
                    prodstock.newprice = after_diff
                    prodstock.save()
                    self.stdout.write(self.style.SUCCESS('[{}] Successfully Updated product id={} with {} price'.format(time.ctime(),product['id'], after_diff)))

                else:
                    serializer = ProduitEnPromotionSerializer(data={'tigID':str(product['id']), 'newprice':after_diff})
                    if serializer.is_valid():
                        serializer.save()
                        self.stdout.write(self.style.SUCCESS('[{}] Successfully added product id={} with {} price'.format(time.ctime(),product['id'], after_diff)))

            else:
                self.stdout.write(self.style.WARNING('[{}] No stock for product id={}'.format(time.ctime(),product['id'])))

        self.stdout.write('['+time.ctime()+'] Data refresh terminated.')
