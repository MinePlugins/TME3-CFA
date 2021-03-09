import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from mytig.config import baseUrl

# Create your views here.
class RedirectionListeDeProduits(APIView):
    def get(self, request, format=None):
        response = requests.get(baseUrl+'products/')
        jsondata = response.json()
        return Response(jsondata)
#    def post(self, request, format=None):
#        NO DEFITION of post --> server will return "405 NOT ALLOWED"

class RedirectionDetailProduit(APIView):
    def get_object(self, pk):
        try:
            response = requests.get(baseUrl+'product/'+str(pk)+'/')
            jsondata = response.json()
            return Response(jsondata)
        except:
            raise Http404
    def get(self, request, pk, format=None):
        response = requests.get(baseUrl+'product/'+str(pk)+'/')
        jsondata = response.json()
        return Response(jsondata)
#    def put(self, request, pk, format=None):
#        NO DEFITION of put --> server will return "405 NOT ALLOWED"
#    def delete(self, request, pk, format=None):
#        NO DEFITION of delete --> server will return "405 NOT ALLOWED"

class RedirectionListeDeShipPoints(APIView):
    def get(self, request, format=None):
        response = requests.get(baseUrl+'shipPoints/')
        jsondata = response.json()
        return Response(jsondata)
#    def post(self, request, format=None):
#        NO DEFITION of post --> server will return "405 NOT ALLOWED"

class RedirectionDetailShipPoint(APIView):
    def get_object(self, pk):
        try:
            response = requests.get(baseUrl+'shipPoint/'+str(pk)+'/')
            jsondata = response.json()
            return Response(jsondata)
        except:
            raise Http404
    def get(self, request, pk, format=None):
        response = requests.get(baseUrl+'shipPoint/'+str(pk)+'/')
        jsondata = response.json()
        return Response(jsondata)

from mytig.models import ProduitEnPromotion,ProduitDisponible
from mytig.serializers import ProduitEnPromotionSerializer, ProduitDisponibleSerializer
from django.http import Http404
from django.http import JsonResponse

class PromoList(APIView):
    def get(self, request, format=None):
        res=[]
        for prod in ProduitEnPromotion.objects.all():
            serializer = ProduitEnPromotionSerializer(prod)
            response = requests.get(baseUrl+'product/'+str(serializer.data['tigID'])+'/')
            jsondata = response.json()
            res.append(jsondata)
        return JsonResponse(res, safe=False)
#    def post(self, request, format=None):
#        NO DEFITION of post --> server will return "405 NOT ALLOWED"
class RemoveSale(APIView):
    def get_object(self, pk):
        try:
            return ProduitEnPromotion.objects.get(tigID=pk)
        except ProduitEnPromotion.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        jsondata = {}
        prod = self.get_object(pk)       
        if prod is not None and prod is not False:
            prod.delete()
            jsondata['message'] = "Successfully delete {} from sale".format(pk)
        return Response(jsondata)

class PutOnSale(APIView):
    def get_object(self, pk):
        try:
            return ProduitEnPromotion.objects.get(tigID=pk)
        except ProduitEnPromotion.DoesNotExist:
            return False
            # raise Http404
    
    def get(self, request, pk, newprice, format=None):
        jsondata = {}
        try:
            newprice = float(newprice)
        except:
            jsondata['message'] = "New price is not a float"
            return Response(jsondata)
        prod = self.get_object(pk)

        response = requests.get(baseUrl+'product/'+str(pk)+'/')
        jsondata_product = response.json()
        jsondata_product["discount"] = newprice
        if response.status_code != 404:
            if prod is not None and prod is not False:
                prod.newprice = newprice
                prod.save()
                serializer = ProduitEnPromotionSerializer(prod)
                jsondata['message'] = "Successfully update {} on sale by {}".format(pk, newprice)
            else:
                serializer = ProduitEnPromotionSerializer(data={'tigID':str(pk), 'newprice':newprice})
                jsondata['message'] = "Successfully put {} on sale by {}".format(pk, newprice)

                if serializer.is_valid():
                    serializer.save()
            jsondata['product'] = jsondata_product
        else:
            jsondata['message'] = "Product ID {} not found".format(pk)
        return Response(jsondata)

class PromoDetail(APIView):
    def get_object(self, pk):
        try:
            return ProduitEnPromotion.objects.get(tigID=pk)
        except ProduitEnPromotion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        prod = self.get_object(pk)
        serializer = ProduitEnPromotionSerializer(prod)
        response = requests.get(baseUrl+'product/'+str(serializer.data['tigID'])+'/')
        jsondata = response.json()
        jsondata["discount"] = serializer.data['newprice']
        jsondata["sale"] = True if serializer.data['newprice'] > 0 else False
        return Response(jsondata)
#    def put(self, request, pk, format=None):
#        NO DEFITION of put --> server will return "405 NOT ALLOWED"
#    def delete(self, request, pk, format=None):
#        NO DEFITION of delete --> server will return "405 NOT ALLOWED"

class DispoList(APIView):
    def get(self, request, format=None):
        res=[]
        for prod in ProduitDisponible.objects.all():
            serializer = ProduitDisponibleSerializer(prod)
            response = requests.get(baseUrl+'product/'+str(serializer.data['tigID'])+'/')
            jsondata = response.json()
            res.append(jsondata)
        return JsonResponse(res, safe=False)
#    def post(self, request, format=None):
#        NO DEFITION of post --> server will return "405 NOT ALLOWED"

class DispoDetail(APIView):
    def get_object(self, pk):
        try:
            return ProduitDisponible.objects.get(pk=pk)
        except ProduitDisponible.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        prod = self.get_object(pk)
        serializer = ProduitDisponibleSerializer(prod)
        response = requests.get(baseUrl+'product/'+str(serializer.data['tigID'])+'/')
        jsondata = response.json()
        return Response(jsondata)