from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from myStockProduct.models import ProductStock
from myStockProduct.serializers import ProductStockSerializer
from django.http import Http404
from django.http import JsonResponse
from mytig.config import baseUrl

# Create your views here.
class ProductsStock(APIView):
    def get(self, request, format=None):
        res=[]
        for prod in ProductStock.objects.all():
            serializer = ProductStockSerializer(prod)
            response = requests.get(baseUrl+'product/'+str(serializer.data['tigID'])+'/')
            jsondata = response.json()
            jsondata['quantityInStock'] = serializer.data['quantityInStock']
            res.append(jsondata)
        return JsonResponse(res, safe=False)
#    def post(self, request, format=None):
#        NO DEFITION of post --> server will return "405 NOT ALLOWED"

class ProductStockDetail(APIView):
    def get_object(self, pk):
        try:
            return ProductStock.objects.get(tigID=pk)
        except ProductStock.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        prod = self.get_object(pk)
        serializer = ProductStockSerializer(prod)
        response = requests.get(baseUrl+'product/'+str(serializer.data['tigID'])+'/')
        jsondata = response.json()
        jsondata['quantityInStock'] = serializer.data['quantityInStock']
        return Response(jsondata)

class DecrStock(APIView):
    def get_object(self, pk):
        try:
            return ProductStock.objects.get(tigID=pk)
        except ProductStock.DoesNotExist:
            raise Http404

    def get(self, request, pk, qty, format=None):
        prod = self.get_object(pk)
        prod.quantityInStock -= qty
        prod.save()
        serializer = ProductStockSerializer(prod)
        response = requests.get(baseUrl+'product/'+str(serializer.data['tigID'])+'/')
        jsondata = response.json()
        jsondata['quantityInStock'] = serializer.data['quantityInStock']
        return Response(jsondata)

class IncrStock(APIView):
    def get_object(self, pk):
        try:
            return ProductStock.objects.get(tigID=pk)
        except ProductStock.DoesNotExist:
            raise Http404

    def get(self, request, pk, qty, format=None):
        prod = self.get_object(pk)
        prod.quantityInStock += qty
        prod.save()
        serializer = ProductStockSerializer(prod)
        response = requests.get(baseUrl+'product/'+str(serializer.data['tigID'])+'/')
        jsondata = response.json()
        jsondata['quantityInStock'] = serializer.data['quantityInStock']
        return Response(jsondata)