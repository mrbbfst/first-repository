from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from SettingsConstants import PlotType, PlotViewType
from sqlalchemy import select
from db_api import Check
from db_api import Session, engine
class PlotsBuilder:
    def __init__(self):
        self.date_from=None
        self.date_to=None
        self.plot_type=None

    def add_date_from(self, date_from):
        self.date_from= datetime.strptime(date_from, "%d.%m.%y")
        return self
    
    def add_date_to(self, date_to):
        self.date_to=datetime.strptime(date_to, "%d.%m.%y")
        return self
    
    def add_plot_type(self, plot_type):
        self.plot_type=plot_type
        return self
    
    def add_plot_view_type(self, plot_view_type):
        self.plot_view_type=plot_view_type
        return self
    
    def build(self):
        query = select(Check)
        if self.date_from is not None:
            query = query.where(Check.time>= self.date_from)
        if self.date_to is not None:
            query = query.where(Check.time<= self.date_to)

        dataset = self.make_dataset(query)
        self.make_plot(dataset)

    def make_dataset(self, query):
        with Session(engine) as session:
            result = session.execute(query)
            dataset = result.scalars().all()
            return dataset
        
    def make_plot(self, dataset):
        delta = timedelta(hours=24)
        # dates = drange(self.date_from, self.date_to, delta)
        x = [d.time for d in dataset]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%d.%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        date_calclate_result = self.date_calculate(dataset, self.plot_type)
        y = [0 if d.date() not in date_calclate_result.keys() else date_calclate_result[d.date()] for d in x]
        
        if self.plot_view_type == PlotViewType.BAR:
            plt.bar(x,y)
        elif self.plot_view_type == PlotViewType.PLOT:
            plt.plot(x,y)
        plt.gcf().autofmt_xdate()
        plt.show()
        
    def date_calculate(self, dataset, plot_type):
        
        if plot_type == PlotType.PLOT_BY_DAY_SUM:
            return self.calculate_plot_by_day_sum(dataset)
        elif plot_type == PlotType.PLOT_BY_DAY_CHECK_COUTN:
            return self.calculate_plot_by_day_check_count(dataset)
        else: 
            return dict()
        
    def calculate_plot_by_day_sum(self, dataset):
        result = dict()
        i = 0
        while i < len(dataset):
            sum = 0
            day = dataset[i].time.date()
            if day in result:
                result[day]+=dataset[i].amount
            else:
                result[day] = dataset[i].amount
            i+=1
        return result
    
    def calculate_plot_by_day_check_count(self, dataset):
        result = dict()
        for check in dataset:
            if check.time.date() in result.keys():
                result[check.time.date()]+=1
            else:
                result[check.time.date()]=1
        return result