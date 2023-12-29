from django.db import models

# Create your models here.

class TradeBookModel(models.Model):
    trade_id=models.AutoField(primary_key=True)
    underlier_ticker=models.CharField(max_length=10)
    product_type=models.CharField(max_length=25)
    payoff=models.CharField(max_length=10)
    trade_date=models.DateField()
    trade_maturity=models.DateField()
    strike=models.FloatField()
    dividend=models.FloatField()

    def __str__(self) -> str:
        return f"trade id: {self.trade_id} underlier_ticker {self.underlier_ticker} product type: {self.product_type} payoff: {self.payoff} trade date: {self.trade_date} "


class Person(models.Model):
    person_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=40)
    company=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    age=models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} -> {self.company} {self.city} {self.age}"


    



      