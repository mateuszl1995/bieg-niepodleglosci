from tkinter import *
from functools import partial
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class GroupsTab:
    
    def __init__(self, tabs):
        self.tab = Frame(tabs)
        tabs.add(self.tab, text = 'Grupy')
        
        self.initFilterFrame()
        self.initExecuteFrame()
        self.initBoxplot()
            
    def groupClick(self, button, group):
        self.groups[group] = not self.groups[group]
        if self.groups[group]:
            button.config(bg='#404040', fg='white')
        else:
            button.config(bg='#f0f0f0', fg='black')
        
    def initFilterFrame(self):
        filterFrame = Frame(self.tab)
        filterFrame.config(bg='blue')
        filterFrame.grid(row=0, column=0, padx=(20,20), pady=(10,0), sticky=N+W)
        
        
        groups = ['M16', 'M20', 'M30', 'M40', 'M50', 'M60', 'M70+',
                        'K16', 'K20', 'K30', 'K40', 'K50', 'K60', 'K70+']
        cellNo = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,18,21]
        self.groups = {}
        for i, group in zip(range(len(groups)), groups):
            b = Button(filterFrame, height=1, width=7*(cellNo[i+1]-cellNo[i]), text=group)
            b.config(border=1, font=('Calibri', 12), command=partial(self.groupClick, b, group))
            b.grid(row=cellNo[i]//7, column=cellNo[i]%7, columnspan=cellNo[i+1]-cellNo[i], sticky=W+E)
            self.groups[group] = False
            if group in ['Mężczyźni', 'Kobiety', 'Wszyscy']:
                self.groupClick(b, group)
            
    def initExecuteFrame(self):
        executeFrame = Frame(self.tab, width=100,height=100)
        executeFrame.config(bg='red')
        executeFrame.grid(row=1, column=0, padx=(20,20), pady=(10,0), sticky=N+W, columnspan=2)
        
        b = Button(executeFrame, height=1, text='Generuj wykres pudełkowy')
        b.config(font=('Calibri', 12), command=self.boxplot)
        b.grid(row=0,column=0,sticky=W)
        
    def initBoxplot(self):
        self.boxplotFrame = boxplotFrame = Frame(self.tab)
        boxplotFrame.grid(row=1, column=0, padx=(20,20), pady=(10,0), sticky='nwes', columnspan=2)
        boxplotFrame.grid_columnconfigure(0, weight=1)
        
        self.fig = fig = Figure(figsize=(7, 4))
        self.ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#f0f0f0')
         
        canvas = FigureCanvasTkAgg(self.fig, master=boxplotFrame)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(row=0, column=0, sticky=EW)
        boxplotFrame.grid_forget()
        
    def boxplot(self):
        self.ax.clear()
        categories = [k for k,v in self.groups.items() if v]
        df = self.df[self.df['category'].isin(categories)]
        df.boxplot(column='time',by='category',ax=self.ax)
        
        self.fig.suptitle('')
        self.ax.set_title('')
        self.ax.set_ylabel('Czas', rotation=0)
        self.ax.yaxis.set_label_coords(-0.05,1.05)
        self.ax.set_xlabel('Kategoria')
        self.ax.set_yticks(np.arange(30*60, 120*60+1, 5*60))
        labels = [self.strTime(int(item)) for item in self.ax.get_yticks().tolist()]
        self.ax.set_yticklabels(labels)
        
        self.fig.canvas.draw()
                
    def setData(self, df, stats):
        self.df = df
        self.stats = stats
        
    def strTime(self, time):
        h = time//3600
        m = time//60 - h*60
        s = time % 60
        return str(h) + ':' + str(m//10) + str(m%10)# + ':' + str(s//10) + str(s%10) 
     
        