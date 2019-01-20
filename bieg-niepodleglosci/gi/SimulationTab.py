from tkinter import *
from functools import partial
#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy.lib.recfunctions import append_fields
import colorsys
import math
#---------End of imports


class SimulationTab:

    def __init__(self, tabs):
        self.tab = Frame(tabs)
        tabs.add(self.tab, text = 'Symulacja')
        
        self.initColorsAndGroups()
        self.initFilterFrame()
        self.initExecuteFrame()
        self.initSimulation()
        
    def initColorsAndGroups(self):
        self.groups = groups = ['K16', 'K20', 'K30', 'K40', 'K50', 'K60', 'K70+', 
                                'M16', 'M20', 'M30', 'M40', 'M50', 'M60', 'M70+']
        colors = ['#ff0080', '#ff00ff', '#ff80ff', '#ff0000', '#ff8000', '#ffff00', '#a0a0a0',  
                  '#c0ffa0', '#00ff00', '#008000', '#00ffff', '#00b0b0', '#0000ff', '#ffffff']
        self.colors = dict(zip(groups, colors))
        
        
    def initSimulation(self):
        fig = plt.Figure(figsize=(7, 4))
        fig.patch.set_facecolor('#f0f0f0')
        
        canvas = FigureCanvasTkAgg(fig, master=self.tab)
        canvas.get_tk_widget().grid(column=0,row=2, padx=(20,20))
        self.ax = ax = fig.add_subplot(111)
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 400)
        ax.axis('equal')
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        self.computeCoordinatesForPlot()
        ax.scatter(self.coordinates['x'], self.coordinates['y'], color='black', s=1)
        self.ani = animation.FuncAnimation(fig, self.animate, interval=20, blit=False)
        fig.tight_layout()
        
    def animate(self, i):
        if not hasattr(self, 'runners') or self.runners is None:
            return
        if hasattr(self, 'scat2'):
            self.scat2.remove()
        time = int(self.simulationTime.get())
        if time > self.overallTime:
            self.stop()
        
        runners = self.runners
        runners['meter'] = 10000 * (time - runners['wait-time']) // runners['time']
        np.clip(runners['meter'], 0, 10000, runners['meter'])
        runners['x'] = [self.coordinates[meter]['x'] for meter in runners['meter']]
        runners['y'] = [self.coordinates[meter]['y'] for meter in runners['meter']]
        scat = self.scat2 = self.ax.scatter(runners['x'], runners['y'], c=runners['color'])
        self.simulationTime.set(time + self.simulationSpeed.get())
        return scat,
    
    def selectRunnersToAnimation(self):
        self.filters['Rok od'] = StringVar(value='')
    
    def initExecuteFrame(self):
        executeFrame = Frame(self.tab, width=100,height=100)
        executeFrame.grid(row=1, column=0, padx=(20,20), pady=(10,0), sticky=N+W, columnspan=2)
        
        b = Button(executeFrame, height=1, text='Start')
        b.config(border=1, font=('Calibri', 12), command=self.start)
        b.grid(row=1,column=0,sticky=W+E)
        
        b = Button(executeFrame, height=1, text='Stop')
        b.config(border=1, font=('Calibri', 12), command=self.stop)
        b.grid(row=1,column=1,sticky=W+E)
        
        b = Button(executeFrame, height=1, text='Zastosuj')
        b.config(border=1, font=('Calibri', 12), command=self.apply)
        b.grid(row=0,column=7,sticky=W, padx=(10,0))
        
        b = Button(executeFrame, height=1, text='Resetuj')
        b.config(border=1, font=('Calibri', 12), command=self.reset)
        b.grid(row=0,column=8,sticky=W, padx=(10,0))
        
        Label(executeFrame, text="Liczność ").grid(row=0,column=0)
        self.runnersNumber = IntVar(value=100)
        Entry(executeFrame, text="", textvariable=self.runnersNumber, width=6).grid(row=0, column=1)
        
        Label(executeFrame, text="Szybkość ").grid(row=0,column=2)
        self.simulationSpeed = IntVar(value=5)
        Entry(executeFrame, text="", textvariable=self.simulationSpeed, width=6).grid(row=0, column=3)
        
        Label(executeFrame, text="Czas ").grid(row=0,column=4)
        self.simulationTime = IntVar(value=0)
        self.simulationTime.trace('w', self.convertTime)
        self.strSimulationTime = StringVar(value=self.strTime(0))
        Entry(executeFrame, text="", textvariable=self.simulationTime, width=6).grid(row=0, column=5)
        Label(executeFrame, textvariable=self.strSimulationTime).grid(row=0,column=6)
        
    def convertTime(self, index, value, op):
        self.strSimulationTime.set(self.strTime(self.simulationTime.get()))
        
    def reset(self):
        self.stop()
        self.simulationTime.set(0)
        
    def start(self):
        if self.simulationTime.get() > self.overallTime:
            self.simulationTime.set(0)
        self.ani.event_source.start()
    def stop(self):
        self.ani.event_source.stop()
    
    def apply(self):
        self.ani.event_source.stop()
        self.constructRunnersForSimulation()
        
    def constructRunnersForSimulation(self):
        groups = self.groups
        colors = self.colors
        selectedCount = 0
        for group in groups:
            selectedCount += self.stats[(group, 'count')] if self.groups[group] else 0
        percentage = self.runnersNumber.get() / selectedCount
        
        self.runners = None
        for group in groups:
            if self.groups[group]:
                c = self.stats[(group, 'count')]
                groupCount = round(c * percentage)
                indexes = np.linspace(0, c-1, groupCount).astype(int)
                runners = self.df[self.df['category'] == group].iloc[indexes][['category', 'time', 'brutto-time']].to_records(index=False)
                self.runners = runners if self.runners is None else np.append(self.runners, runners)
        
        self.runners = append_fields(self.runners, 'wait-time', self.runners['brutto-time'] - self.runners['time'])    
        self.runners = append_fields(self.runners, 'x', self.runners['brutto-time']*0)    
        self.runners = append_fields(self.runners, 'y', self.runners['brutto-time']*0)    
        self.runners = append_fields(self.runners, 'meter', self.runners['brutto-time']*0)    
        self.runners = append_fields(self.runners, 'color', np.array([colors[category] for category in self.runners['category']]))
        self.overallTime = max(self.runners['brutto-time'])
        
    def computeCoordinatesForPlot(self):
        y_margin = 50
        x_margin = 50
        w = 600
        h = int(w * 2 / (math.pi+2))
        r = h//2 # radius
        l = math.pi * r # line length
        
        coordinates = np.zeros(10001, dtype=[('x', int), ('y', int)])
        for meter in range(2500):
            p = (meter % 2500) / 2500 # part of stage from 0 to 1
            y = h
            x = r + l * p
            coordinates[meter] = (int(x), int(y))
        for meter in range(2500, 5000):
            p = (meter % 2500) / 2500 # part of stage from 0 to 1
            alpha = math.pi * (0.5-p)
            y = r + r*math.sin(alpha)
            x = r + l + r*math.cos(alpha)
            coordinates[meter] = (int(x), int(y))
        for meter in range(5000, 7500):
            p = (meter % 2500) / 2500 # part of stage from 0 to 1
            y = 0
            x = r+ l * (1-p)
            coordinates[meter] = (int(x), int(y))
        for meter in range(7500, 10000):
            p = (meter % 2500) / 2500 # part of stage from 0 to 1
            alpha = math.pi * (1.5 - p)
            y = r + r*math.sin(alpha)
            x = r+ r*math.cos(alpha)
            coordinates[meter] = (int(x), int(y))
        coordinates[10000] = coordinates[0]
        
        coordinates['x'] += x_margin
        coordinates['y'] += y_margin
        self.coordinates = coordinates
        
    def initFilterFrame(self):
        filterFrame = Frame(self.tab)
        filterFrame.config(bg='blue')
        filterFrame.grid(row=0, column=0, padx=(20,20), pady=(10,0), sticky=N+W)
        
        
        groups = self.groups
        cellNo = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18,21]
        self.groups = {}
        for i, group in zip(range(len(groups)), groups):
            b = Button(filterFrame, height=1, width=7*(cellNo[i+1]-cellNo[i]), text=group)
            b.config(border=1, font=('Calibri', 12), command=partial(self.groupClick, b, group))
            b.grid(row=cellNo[i]//7, column=cellNo[i]%7, columnspan=cellNo[i+1]-cellNo[i], sticky=W+E)
            self.groups[group] = False
            if group in ['Mężczyźni', 'Kobiety', 'Wszyscy']:
                self.groupClick(b, group)
                
    def groupClick(self, button, group):
        self.groups[group] = not self.groups[group]
        if self.groups[group]:
            button.config(bg=self.colors[group])
        else:
            button.config(bg='#f0f0f0')
            
    def setData(self, df, stats):
        self.df = df
        self.stats = stats
            
    def strTime(self, time):
        h = time//3600
        m = time//60 - h*60
        s = time % 60
        return str(h) + ':' + str(m//10) + str(m%10) + ':' + str(s//10) + str(s%10) 
        