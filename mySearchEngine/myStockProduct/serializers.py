from rest_framework.serializers import ModelSerializer
from myStockProduct.models import ProductStock

class ProductStockSerializer(ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ('id', 'tigID', 'quantityInStock')
