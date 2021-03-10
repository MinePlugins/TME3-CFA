from django.core.management.base import BaseCommand, CommandError
from myStockProduct.models import ProductStock
from myStockProduct.serializers import ProductStockSerializer
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
        ProductStock.objects.all().delete()
        for product in jsondata:
            if product['availability']: # Verification de la disponibilité et création d'un stock aléatoire
                serializer = ProductStockSerializer(data={'tigID':str(product['id']), 'quantityInStock':randrange(1, 30)})
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(self.style.SUCCESS('['+time.ctime()+'] Successfully added product id="%s"' % product['id']))

            else:
                serializer = ProductStockSerializer(data={'tigID':str(product['id']), 'quantityInStock':0})
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(self.style.SUCCESS('['+time.ctime()+'] Successfully added product id="%s"' % product['id']))

        self.stdout.write('['+time.ctime()+'] Data refresh terminated.')
