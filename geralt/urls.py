from django.urls import path
from . import views

app_name='geralt'

urlpatterns=[path("", views.starting_page, name="starting-page"),
             path("trade_book",views.prepare_form, name="trade-book"),
             path("trade_book/<int:trade_id>",views.single_trade, name="single-trade"),
             path("pricing environment", views.pricing_environment,name="pricing-environment")] 
