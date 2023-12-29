from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect,JsonResponse
from django.core.serializers import serialize
from django.template.loader import render_to_string
import json
from .models import Person,TradeBookModel
from .src.geralt.pricing_environment.pricing_environment import TradeCalendarSchedule,MarketEnvironment
from .forms import CompanyForm



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

# --------------------------
# Region source code objectsvis
# --------------------------



# --------------------------
# End Region source code objects
# --------------------------


# --------------------------
# Region Rendering page app
# --------------------------
def starting_page(request):
    
    return render(request,"geralt/index.html")


def prepare_form(request):
    

    all_trades=TradeBookModel.objects.all()
    serialized_data=serialize("json",all_trades)
    serialized_data=json.loads(serialized_data)
    return render(request,"geralt/trade_book.html",{"trades":serialized_data}) 

def single_trade(request,trade_id:int):
    single_trade=TradeBookModel.objects.get(pk=trade_id)
    return render(request,'geralt/single_trade.html',{"single_trade":single_trade})

  
    

    
                 
def pricing_environment(request):
    pass

# --------------------------
# End Region Rendering page app
# --------------------------
