from django.urls import path
from . import views

urlpatterns=[path("", views.starting_page, name="starting-page"),
             path("trade_book",views.trade_details, name="trade-book"),
             path("pricing environment", views.pricing_environment), 
             path("pricing environment/<slug>", views.pricing_environment)]
