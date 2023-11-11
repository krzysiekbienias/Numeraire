from ...geralt.market_data_domain.yahooDataExtractor import YahooDataExtractor
from ...geralt.tool_kit.QuantLibToolKit import QuantLibToolKit
from ....models import TradeBookModel

import QuantLib as ql
from datetime import datetime
import os
import pandas as pd
from typing import TypeVar, Iterable, Tuple, Dict, List, Generic, NewType





QL = NewType("QL", ql)

DT = TypeVar('DT')



class TradeCalendarSchedule():

    def __init__(self,
                 valuation_date: str="2023-4-22",
                 termination_date: str="2023-7-22",
                 calendar: str = "theUK",
                 year_fraction_convention: str = "Actual365",
                 frequency: str = "monthly",
                 **kwargs):
        """
        Description
        -----------
        This class sets up generic the environment for pricing different financial instruments.

        Parameters
        ----------
        valuation_date : str
            The date you want to price financial instrument. Format Y-m-d.

        termination_date : str
            Date after which your trade expires. Format Y-m-d.
        calendar : str, optional
            Name of the specific calendar of dates to follow, by default "theUK". It corresponds with name of country.
        Possible calendar to chose:
        - theUk
        - USA
        - Poland
        - Switzerland
        year_fraction_convention : str, optional
            Name of year count convention that sets rule how year fraction to be calculated, by default "Actual365"
            Another possible:
            - Actual360, 
            - Actual365,
            - ActualActual,
            - Thirty360
            - Business252 
        frequency : str, optional
            Name of frequency according to with tenors are generated. In particular daily if we want to have business days in our schedule,
              by default "monthly"
            Possible parameters:
            - daily
            - once
            - monthly
            - quarterly
            - annual
            - semiannual


        Note
        ----
        Please note that within this class as well as QuantLibToolKid are defined different static methods where variable are converted into.
        This interface allows to User do not take care about it.

        """

        # -----------------------
        # Region: Constructors
        # -----------------------
        self._valuation_date = valuation_date
        self._termination_date = termination_date
        self._s_calendar = calendar
        self._s_year_fraction_conv = year_fraction_convention
        self._s_frequency = frequency
        # -----------------------
        # END Region: Constructors
        # -----------------------

        # ----------------------------
        # Region: Processing input data
        # ----------------------------

        self.process_trade_info_data()

        # -----------------------
        # END Processing input data
        # -----------------------


        # -----------------------
        # Region: QuantLib Converter
        # -----------------------
        ql_valuation_date = QuantLibToolKit.string_2qlDate(
            date=self._valuation_date)
        ql_termination_date = QuantLibToolKit.string_2qlDate(
            date=self._termination_date)
        date_correction_schema = QuantLibToolKit.set_date_corrections_schema()
        ql_year_fraction_conv = self.set_year_fraction_convention(
            year_fraction_conv=self._s_year_fraction_conv)
        ql_calendar = QuantLibToolKit.set_calendar(country=self._s_calendar)

        ql_schedule = self.set_schedule(effectiveDate=ql_valuation_date,
                                       terminationDate=ql_termination_date,
                                       tenor=ql.Period(QuantLibToolKit.set_frequency(
                                           freq_period=self._s_frequency)),
                                       calendar=ql_calendar)
        # -----------------------
        # Region: QuantLib Converter
        # -----------------------

        # -----------------------
        # Region: Attributes
        # -----------------------
        self.scheduled_dates = list(ql_schedule)
        self.year_fractions = self.get_year_fraction_sequence(schedule=ql_schedule,
                                                           convention=ql_year_fraction_conv)
        self.days_until_expiration=self.scheduled_dates[-1]-self.scheduled_dates[0]
        # -----------------------
        # End Region: Attributes
        # -----------------------

    # -----------------------
    # Region: getters
    # -----------------------
    def get_valuation_date(self):
            return self._valuation_date
        
    def get_termination_date(self):
        return self._termination_date
    
    def get_calendar_name(self):
        return self._s_calendar
    
    def get_year_fraction_convention_name(self):
        return self._s_year_fraction_conv
    
    def get_frequency(self):
        return self._s_frequency
    # -----------------------
    # End Region: getters
    # -----------------------
   

    # -----------------------
    # Region: setters
    # -----------------------        
    def set_valuation_date(self,valuation_date):
        self._valuation_date=valuation_date

    def set_termination_date(self,termination_date):
        self._termination_date=termination_date

    def set_calendar(self,calendar):
        self._s_calendar=calendar
    
    def set_year_fraction_convention_name(self,year_fraction_convention):
        self._s_year_fraction_conv=year_fraction_convention

    def set_frequency(self,frequency):
        self._s_frequency=frequency
    # -----------------------
    # END Region: setters
    # -----------------------

    def process_trade_info_data(self,id=None,*args,**kwargs):
    
            
        valuation_date=args[0] if len(args)>0 else  kwargs["valuation_date"] if "valuation_date" in kwargs else self.get_valuation_date()
        # termination_date
        termination_date=args[1] if len(args)>1 else  kwargs["valuation_date"] if "valuation_date" in kwargs else self.get_termination_date()
        #calendar_name
        calendar_name=args[2] if len(args)>2 else  kwargs["calendar_name"] if "calendar_name" in kwargs else self.get_calendar_name()
        #year_convention
        year_convention=args[3] if len(args)>3 else  kwargs["year_convention"] if "year_convention" in kwargs else self.get_year_fraction_convention_name()
        #frequency
        year_frequency=args[4] if len(args)>4 else  kwargs["year_frequency"] if "year_frequency" in kwargs else self.get_frequency()
        
        params_set={
                "valuation_date":valuation_date,
                "termination_date":termination_date,
                "calendar_name":calendar_name,
                "year_convention":year_convention,
                "year_frequency":year_frequency}

        return params_set



    def parse_trade_attributes_from_db(self,id):

        one_trade_from_db=TradeBookModel().objects.get(id)
        return one_trade_from_db



            



        


    def set_year_fraction_convention(self, year_fraction_conv: str = "Actual365") -> QL:
        """set_year_fraction_convention
        Description
        -----------
        Function defines how we will calculate year fraction.

        Parameters
        ----------
        year_fraction_conv : string
             Available alternatives: Actual360, Actual365, ActualActual, Thirty360, Business252


        Returns
        -------
        ql.FractionConvention

        """
        if (year_fraction_conv == 'Actual360'):
            day_count = ql.Actual360()
            return day_count
        elif (year_fraction_conv == 'Actual365'):
            day_count = ql.Actual365Fixed()
            return day_count
        elif (year_fraction_conv == 'ActualActual'):
            day_count = ql.ActualActual()
            return day_count
        elif (year_fraction_conv == 'Thirty360'):
            day_count = ql.Thirty360()
            return day_count
        elif (year_fraction_conv == 'Business252'):
            day_count = ql.Business252()
            return day_count


    def set_schedule(self,
                    effectiveDate: ql.Date,
                    terminationDate: ql.Date,
                    tenor: ql.Period,
                    calendar: ql.Calendar,
                    convention=QuantLibToolKit.set_date_corrections_schema(),
                    termination_date_convention=QuantLibToolKit.set_date_corrections_schema(),
                    rule: ql.DateGeneration = QuantLibToolKit.set_rule_of_date_generation(date_generation_rules="forward"),
                    endOfMonth: bool = False) -> ql.Schedule:
        """set_schedule
        Description
        -----------
        Method creates the schedule that handle with life cycle of a trade. The heart of the class.

        Parameters
        ----------
        effectiveDate : ql.Date
            _description_
        terminationDate : ql.Date
            _description_
        tenor : ql.Period
            _description_
        calendar : ql.Calendar
            _description_
        convention : _type_, optional
            _description_, by default QuantLibToolKit.set_date_corrections_schema()
        termination_date_convention : _type_, optional
            _description_, by default QuantLibToolKit.set_date_corrections_schema()
        rule : ql.DateGeneration, optional
            _description_, by default QuantLibToolKit.setRuleOfDateGeneration()
        endOfMonth : bool, optional
            _description_, by default False

        Returns
        -------
        ql.Schedule
            _description_
        """

        return ql.Schedule(effectiveDate, terminationDate, tenor, calendar, convention, termination_date_convention, rule, endOfMonth)

    def get_year_fraction_sequence(self,
                                schedule: ql.Schedule,
                                convention: QL) -> List[float]:
        """consecutiveDatesYearFraction
        Description
        -----------
        For given sequence of dates returns arr of list year fractions with edges T_i-1 and T_i


        Returns
        -------
        List[float]
            list of year fraction's
        """
        lf_year_fraction = []
        scheduled_dates = list(schedule)
        if len(scheduled_dates) == 2:
            # frequency probably set as 'once' so only valuation and termination date has been provided
            return convention.yearFraction(scheduled_dates[0], scheduled_dates[1])
        for i in range(1, len(scheduled_dates)):
            temp_yf = convention.yearFraction(
                scheduled_dates[i-1], scheduled_dates[i])
            lf_year_fraction.append(temp_yf)
        return lf_year_fraction

    def display_schedule(self) -> None:
        """display_schedule
        Description
        -----------
        This method display information about schedule.
        """

        dates = self.scheduled_dates
        if len(dates) == 2:
            print("At valuation date there is still {0:.2f} of the year.".format(
                self.year_fractions))
        else:
            year_fractions = [None]+self.year_fractions
            df_schedule = pd.DataFrame(zip(dates, year_fractions), columns=[
                                       'Calendar_Grid', "Year_Fraction"])
            print(df_schedule)


class MarketEnvironmentInterface:
    def extract_underlier_quotation(self):
        pass

    def extract_volatility(self):
        pass
    
    def extract_discount_factors(self):
        pass

    def validate_market_data(self):
        pass

    def process_parameters(self):
        pass



class MarketEnvironment:
    def __init__(self,
                 valuation_date:str="2023-10-02", #remember to add zero for 
                 underliers:(str,List[str])="TSLA",
                 risk_free_rate:float=0.06,
                 volatility:float=0.32
                 ):
        """__init__
        Description
        -----------
        Market data object for pricing derivative instruments. It is not defined in trade attributes but comes directly from market.

        Parameters
        ----------
        market_date : str
            _description_
        underlier_price : float
            _description_
        risk_free_rate : float
            _description_
        implied_volatility : float
            _description_
        """
        self._valuation_date=valuation_date
        self._underliers=underliers
        self._risk_free_rate=risk_free_rate
        self._volatility=volatility


    # --------------
    # Region getters
    # --------------
    def get_valuation_date(self):

            return self._valuation_date
    
    def get_underliers(self):
        return self._underliers
    
    def get_risk_free_rate(self):
        return self._risk_free_rate
    
    def get_volatility(self):
        return self._volatility
    

    # --------------
    # End  Region getters
    # --------------

    # --------------
    # Region setters
    # --------------
    def set_valuation_date(self,valuation_date):
            self._valuation_date=valuation_date
    
    def set_underliers(self,underlier_price):
            self._underlier_price=underlier_price
    
    def set_risk_free_rate(self,risk_free_rate):
        self._risk_free_rate=risk_free_rate

    def set_volatility(self,volatility):
        self._volatility=volatility

    # --------------
    # End  Region getters
    # --------------

    def extract_underlier_quotation(self) -> dict:
        return YahooDataExtractor(tickers=self._underliers,start_period=self._valuation_date).extract_data()

    
        
    def get_discount_factors(self, maturity_date:str):
        rate=ql.InterestRate(self._risk_free_rate,ql.Actual365Fixed,2,0)
        return rate.discountFactor(self._valuation_date,maturity_date)
    
    def process_market_parameters(self,*args,**kwargs)->dict:
        """process_market_parameters 
        Description
        Utility method to parse option price that comes from market. It supports defining parameters by user when the method is called as well as feeding parameters from
        diverse data providers.

        Returns
        -------
        dict
            _description_
        """

        # underlying value at valuation date
        underlying_price= args[0] if len(args)>0 else kwargs["underlier_price"] if "underlier_price" in kwargs else self.extract_underlier_quotation()
        # risk free rate
        risk_free_rate=args[1] if len(args)>1 else kwargs['risk_free_rate'] if "risk_free_rate" in kwargs else self.get_risk_free_rate()
        # volatility
        volatility=args[2] if len(args)>2 else kwargs['volatility'] if "volatility" in kwargs else self.get_volatility()
        return {"underlying_price":underlying_price,
                "risk_free_rate":risk_free_rate,
                "volatility":volatility}



        
        


        
    def validate_market_data(self):
        raise NotImplementedError()


    def display_market_data(self):
        def __str__(self) -> str:

            return f'Market data:\n Underlier Price :{self._underlier_price} \n Risk free rate for pricing :{self._risk_free_rate}\n Implied volatility: {self._implied_volatility}\n '
        


        


