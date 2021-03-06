from django.urls import path
from mytig import views

urlpatterns = [
    path('products/', views.RedirectionListeDeProduits.as_view()),
    path('product/<int:pk>/', views.RedirectionDetailProduit.as_view()),
    path('availableproducts/', views.DispoList.as_view()),
    path('availableproduct/<int:pk>/', views.DispoDetail.as_view()),
    path('shipPoints/', views.RedirectionListeDeShipPoints.as_view()),
    path('shipPoint/<int:pk>/', views.RedirectionDetailShipPoint.as_view()),
    path('onsaleproducts/', views.PromoList.as_view()),
    path('onsaleproduct/<int:pk>/', views.PromoDetail.as_view()),
]
