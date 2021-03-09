from django.db import models

class ProductStock(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tigID = models.IntegerField(default='-1')
    quantityInStock = models.IntegerField(default='0')

    class Meta:
        ordering = ('tigID',)

