from gi.GroupsTab import GroupsTab
from gi.RunnersDataTab import RunnersDataTab
from gi.RunnersStatsTab import RunnersStatsTab
from gi.SimulationTab import SimulationTab
from gi.MapTab import MapTab
import os.path
from tkinter import *

import pandas as pd
from gi.SimulationTab import SimulationTab


class MainApp:
    def __init__(self, window):
        self.window = window
        self.size = '920x600'
        window.title("Bieg niepodległości")
        
        self.initMenu()
        
        #self.mode = IntVar(None, 1)
        #modes = Frame(window)
        #modes.pack(anchor=NW)
        #Radiobutton(modes, text="Dane", variable=self.mode, value=1).pack(side=LEFT)
        #Radiobutton(modes, text="Statystyki", variable=self.mode, value=2).pack(side=LEFT)
        
        tabs = ttk.Notebook(window)
        self.runnersDataTab = RunnersDataTab(tabs)
        self.runnersStatsTab = RunnersStatsTab(self.runnersDataTab.tab)
        self.groupsTab = GroupsTab(tabs)
        self.simulationTab = SimulationTab(tabs)
        self.mapTab = MapTab(tabs)
#         locationsTab = Frame(tabs)
        
#         tabs.add(locationsTab, text = 'Miejscowości')       
        tabs.pack(expand=1, fill=BOTH)
        tabs.select(self.mapTab.tab)
        
        
        self.open()
        
        window.overrideredirect(True)
        window.overrideredirect(False)
        
    
        
    def initMenu(self):
        menubar = Menu(self.window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Otwórz", command=self.open)
        menubar.add_cascade(label="Plik", menu=filemenu)
        window.config(menu=menubar)
        
    def open(self, path=''):
#         path = filedialog.askopenfilename(initialdir = "./data",title = "Wybierz plik", filetypes = (("Pliki CSV","*.csv"),("Wszystkie pliki","*.*")))
        path = '../data/bieg-2018.csv'
        if path == '':
            return
        
        self.df = df = pd.read_csv(path, ';')
        self.path = path
        filename = os.path.split(self.path)[-1]
        self.window.title("Bieg niepodległości - " + filename)
        
        self.computeStats()
        self.runnersDataTab.setData(df)   
        self.runnersStatsTab.setData(df, self.stats) 
        self.groupsTab.setData(df, self.stats) 
        self.simulationTab.setData(df, self.stats)
        self.mapTab.setData(df, self.stats)  
        self.runnersDataTab.setListeners([self.runnersStatsTab])
        self.window.after(100, self.groupsTab.boxplotFrame.grid)
        
    def computeStats(self):
        stats = {}
        df = self.df
        
        df = df.groupby(['category'])['time'];
        measureResults = [df.count(), df.mean(), df.min(), df.max()]
        measureNames = ['count', 'mean', 'min', 'max']
        
        for measureName, measureResult in zip(measureNames, measureResults):
            for categoryName, result in measureResult.items():
                stats[(categoryName, measureName)] = result 
        
        df = self.df
        dfMen = df.loc[df['place-M'] != -1]['time']
        dfWomen = df.loc[df['place-W'] != -1]['time']
        dfAll = df['time']
        
        for key, df in zip(['M', 'K', 'ALL'], [dfMen, dfWomen, dfAll]):
            measureResults = [df.count(), df.mean(), df.min(), df.max()]
            measureNames = ['count', 'mean', 'min', 'max']
            for name, result in zip(measureNames, measureResults):
                stats[(key, name)] = result  
                    
        self.stats = stats

window = Tk()
my_gui = MainApp(window)
window.geometry(my_gui.size)
window.mainloop()