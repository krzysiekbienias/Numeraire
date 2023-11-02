from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.template.loader import render_to_string
from .models import Person


# Create your views here.

trades_all=  [{

    "Trade_Id": 'eo_1',
    "Underlier_Ticker": 'APPL',
    "Product_Type": 'European Option',
    "Payoff": 'Call',
    "Trade_Date": '2023-4-23',
    "Trade_Maturity": '2023-7-23',
    "Strike": 67,
    "Dividend": 0
  },
  {
    
    "Trade_Id": 'eo_2',
    "Underlier_Ticker": 'APPL',
    "Product_Type": 'European Option',
    "Payoff": 'Put',
    "Trade_Date": '2023-4-23',
    "Trade_Maturity": '2023-10-23',
    "Strike": 67,
    "Dividend": 0
  },
  {
    "Trade_Id": 'eo_3',
    "Underlier_Ticker": 'MSI',
    "Product_Type": 'European Option',
    "Payoff": 'Put',
    "Trade_Date": '2023-4-23',
    "Trade_Maturity": '2023-5-23',
    "Strike": 27.5,
    "Dividend": 0
  }]


def starting_page(request):
    return render(request,"geralt/index.html")


def trade_details(request):
    return render(request,"geralt/trade_book.html",{"trades":trades_all}) 

    
                 
def pricing_environment(request):
    pass
