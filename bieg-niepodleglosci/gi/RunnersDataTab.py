from tkinter import *
from pandastable import Table
import re

class RunnersDataTab:
    def __init__(self, tabs):
        self.tab = Frame(tabs)
        tabs.add(self.tab, text = 'Zawodnicy')
        
        self.headerFrame = Frame(self.tab)
        self.tableFrame = Frame(self.tab)  
        self.headerFrame.pack(side=TOP, anchor='w')
        self.tableFrame.pack(anchor='w')
        
        self.initFilter()
        
    
    def setData(self, df):
        df = df.copy()
        df = df.drop(columns=['team', 'place-category', 'place-M', 'place-W', 's-half-time', 's-brutto-time', 'time', 'half-time', 'brutto-time'])
        df.columns = ['Lp', 'Numer', 'Imię', 'Nazwisko', 'Miejscowość', #'Drużyna', 
                      'Rocznik', 'Kategoria', 'Czas']
        self.df = df
        self.applyFilter()
        
    def initFilter(self):
        self.filters = {}
        cols = ['', 'Imię', 'Nazwisko', 'Kategoria', 'Miejscowość', 'Rok od', 'Rok do']
        widths = [0, 20, 20, 10, 20, 7, 7]
        self.filters['Rok od'] = StringVar(value='')
        self.filters['Rok do'] = StringVar(value='')
        
        for col in range(len(cols)):
            text = cols[col]
            label = Label(self.headerFrame, text=text)
            label.grid(row=0, column=col, sticky='W')
            if col > 0:
                if col < 5:
                    self.filters[text] = StringVar(value='')
                entry = Entry(self.headerFrame, text="", textvariable=self.filters[text])
                entry.config(width=widths[col])
                entry.grid(row=1, column=col)
            else:
                label.config(width=7)
        btn = Button(self.headerFrame, text='Filtruj', command=self.applyFilter)
        btn.grid(row=1, column=len(cols)+1)
        btnClear = Button(self.headerFrame, text='Czyść', command=self.clearFilters)
        btnClear.grid(row=1, column=len(cols)+2)
        
    def applyFilter(self): 
        df = self.df
        minYear = 0
        maxYear = 10000
        try:
            minYear = int(self.filters['Rok od'].get())
            maxYear = int(self.filters['Rok do'].get())
        except:
            pass
        self.filterData = df[df['Imię'].str.contains(self.filters['Imię'].get(), flags=re.I) \
           & df['Nazwisko'].str.contains(self.filters['Nazwisko'].get(), flags=re.I) \
           & df['Kategoria'].str.contains(self.filters['Kategoria'].get(), flags=re.I) \
           & df['Miejscowość'].str.contains(self.filters['Miejscowość'].get(), flags=re.I) \
           & (df['Rocznik'] >= minYear) \
           & (df['Rocznik'] <= maxYear)   ] 
        self.refersh()
        
    def refersh(self):
        self.tableFrame.destroy()
        self.tableFrame = Frame(self.tab)
        self.table = MyTable(self.tableFrame, dataframe=self.filterData, showtoolbar=False)
        self.table.show() 
        self.tableFrame.pack(fill=BOTH, expand=1)
        try:
            self.table.listeners = self.listeners
        except:
            pass
        
    def clearFilters(self):
        self.filters['Rok od'].set('')
        self.filters['Rok do'].set('')
        for col in ['Imię', 'Nazwisko', 'Kategoria', 'Miejscowość']:
            self.filters[col].set('')
        self.applyFilter()
            
    def setListeners(self, listeners):
        self.listeners = self.table.listeners = listeners
          
class MyTable(Table):
    def handle_left_click(self, event):
        Table.handle_left_click(self, event)
        self.notifyChangeRunner()
         
    def handle_arrow_keys(self, event):
        Table.handle_arrow_keys(self, event)
        self.notifyChangeRunner()
        
    def notifyChangeRunner(self):
        row = int(self.getSelectedRow())
        runner = self.model.df.iloc[row]
        for listener in self.listeners:
            listener.changeRunner(runner)
    
            
            
    