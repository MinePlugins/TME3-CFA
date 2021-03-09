from django.urls import path, register_converter, re_path


from mytig import views

class FloatUrlParameterConverter:
    regex = '[0-9]+\.?[0-9]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatUrlParameterConverter, 'floatsss')

urlpatterns = [
    path('products/', views.RedirectionListeDeProduits.as_view()),
    path('product/<int:pk>/', views.RedirectionDetailProduit.as_view()),
    path('availableproducts/', views.DispoList.as_view()),
    path('availableproduct/<int:pk>/', views.DispoDetail.as_view()),
    path('shipPoints/', views.RedirectionListeDeShipPoints.as_view()),
    path('shipPoint/<int:pk>/', views.RedirectionDetailShipPoint.as_view()),
    path('onsaleproducts/', views.PromoList.as_view()),
    path('onsaleproduct/<int:pk>/', views.PromoDetail.as_view()),
    path('putonsale/<int:pk>/<floatsss:newprice>/', views.PutOnSale.as_view()),
    path('removesale/<int:pk>/', views.RemoveSale.as_view()),
]
