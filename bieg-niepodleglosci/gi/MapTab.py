from tkinter.ttk import Frame
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import math
import pandas as pd

class MapTab:

    def __init__(self, tabs):
        self.tab = Frame(tabs)
        tabs.add(self.tab, text = 'Mapa uczestników')
        
        fig = plt.Figure(figsize=(6, 5.5))
        fig.patch.set_facecolor('#f0f0f0')
        
        canvas = FigureCanvasTkAgg(fig, master=self.tab)
        canvas.get_tk_widget().grid(column=0,row=2, padx=(20,20))
        self.ax = ax = fig.add_subplot(111)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('equal')
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        fig.tight_layout()
        self.img = plt.imread("../img/map.png")
        
        self.loadGeolocations()
        
    def loadGeolocations(self):
        geo = pd.read_csv('../data/geolocations.csv', ';')
        intab = "ąćęłńóśźż"
        outtab = "acelnoszz"
        self.translateTable = str.maketrans(intab, outtab)
        geo['location2'] = geo['location'].str.lower().str.translate(self.translateTable)
        self.geo = {}
        for index, row in geo.iterrows():
            key = row['location2']
            value = (row['n'], row['e'])
            self.geo[key] = value
        
    def setData(self, df, stats):
        df['location2'] = df['location'].str.lower().str.translate(self.translateTable)   
        locations = df['location2'].astype(str).values
        self.locations, self.counts = np.unique(locations, return_counts=True)
        self.x = [self.getX(location) for location in self.locations]
        self.y = [self.getY(location) for location in self.locations]
        self.counts = [int(count**0.6) for count in self.counts]
        
        self.makePlot()
        
    def getX(self, location):
        # 15-1100, 14.12-24.15
        null_key = (52.4,16.9)
        e = self.geo.get(location, null_key)[1]
        n = self.geo.get(location, null_key)[0]
        x = 15 + (e-14.12) * (1100-15) / (24.15-14.12)
        return x
    
    def getY(self, location):
        # 50-1050, 49.0-54.8
        null_key = (52.4,16.9)
        n = self.geo.get(location, null_key)[0]
        y = 50 + (54.8-n) * (1050-50) / (54.8-49.0)
        return y
     
        
    def makePlot(self):
        ax = self.ax
        ax.cla()
        ax.imshow(self.img)
        
        ax.scatter(self.x, self.y, color='blue', s=self.counts)
        
        