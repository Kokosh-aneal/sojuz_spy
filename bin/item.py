#! /usr/bin/python3

from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import  matplotlib.ticker as ticker
import sys

class Item:
#Item class constructor
    def __init__(self,ID,name,key,log,host_name,units):
        self.ID = ID
        self.name = name
        self.host_name = host_name
        self.key = key
        self.log = log
        self.x = []
        self.y = []
        self.units = units

#Function which creates plots and saves them in tmp directory (changed in Report class)
    def gen_graph(self):
        self.log.append(2,'Generating {} graph'.format(self.name))
        dates = mdates.date2num(self.x)
        plt.figure(figsize=(20,5))
        plt.plot_date(dates,self.y,'r')
        plt.title(self.name)
        option = sys.argv[1:]
        option = option[0]
        if option == '-d':
            loc = mdates.HourLocator(interval=1)
            fmt = mdates.DateFormatter('%H:%M')
            label = 'Time [h:m]'
        elif option == '-m':
            loc = mdates.DayLocator(interval=1)
            fmt = mdates.DateFormatter('%m.%d')
            label = 'Day [m.d]'
        elif option == '-w':
            loc = mdates.DayLocator(interval=1)
            fmt = mdates.DateFormatter('%d')
            label = 'Day [m.d]'
        plt.gca().xaxis.set_major_formatter(fmt)
        plt.gca().xaxis.set_major_locator(loc)
        plt.ticklabel_format(axis='y',style='plain')
        plt.gca().yaxis.set_major_formatter(ticker.EngFormatter(unit=self.units))
        plt.grid()
        plt.xlabel(label)
        if self.units == '':
            plt.ylabel('[amount]')
            plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        else:
            plt.ylabel('['+self.units+']')
        plt.savefig(self.ID+'.jpg')
        plt.close()
