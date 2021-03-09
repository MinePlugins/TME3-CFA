from django.urls import path
from myStockProduct import views

urlpatterns = [
    path('myStockProduct/infoproducts/', views.ProductsStock.as_view()),
    path('myStockProduct/infoproduct/<int:pk>/', views.ProductStockDetail.as_view()),
    path('myStockProduct/incrementStock/<int:pk>/<int:qty>/', views.IncrStock.as_view()),
    path('myStockProduct/decrementStock/<int:pk>/<int:qty>/', views.DecrStock.as_view()),
]
