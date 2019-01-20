from tkinter import *
from PIL import ImageTk, Image

class RunnersStatsTab:
    def __init__(self, tabs):
        self.tab = tab = Frame(tabs)
        tab.pack(side=BOTTOM, anchor='w', padx=(20,0))
        #tabs.add(self.tab, text = 'Zawodnicy - statystyki')
        self.loadImages()
        
        f = Frame(self.tab, height=300, width=200)
        f.grid(row=0, column=0, sticky='w', pady=(10,0))
                
        Label(f, text='Porównaj z:').grid(row=0,column=0, sticky='w')
        self.combo = StringVar(value='Wszyscy')
        self.combo.trace('w', self.comboCallback)
        categories = ['Wszyscy', 'Mężczyźni', 'Kobiety', 'M16', 'M20', 'M30', 'M40', 'M50', 'M60', 'M70+', 'K16', 'K20', 'K30', 'K40', 'K50', 'K60', 'K70+']
        self.comboBox = comboBox = ttk.Combobox(f, text='Kategoria', values=categories, textvar=self.combo, state="readonly")
        comboBox.grid(row=0,column=1,padx=(10, 0), columnspan=4, sticky='nw')
        comboBox.bind("<FocusIn>", self.defocus)
        
        self.comment1 = StringVar(value='')
        self.comment2 = StringVar(value='')
#         l = Message(tab, textvariable=self.comment1)
#         l.grid(row=1,column=0,sticky='nw', columnspan=4, padx=20)
#         l.config(width = 600, font=("Calibri", 12))
        
        self.canvas = canvas = Canvas(tab, width=995, height=35, bg='#f0f0f0')
        canvas.grid(row = 3, column = 0, columnspan=4, padx=20, pady=(0, 0), sticky='sw')
        l = Label(tab, textvariable=self.comment1)
        l.grid(row=4, column=0, sticky='nw', padx=20, pady=0)
        l.config(font=("Calibri", 12))
        
        self.canvas2 = canvas2 = Canvas(tab, width=995, height=35, bg='#f0f0f0', selectbackground='#ffffff')
        canvas2.grid(row = 5, column = 0, columnspan=4, padx=20, pady=(20, 0), sticky='sw')
        l = Label(tab, textvariable=self.comment2)
        l.grid(row=6, column=0, sticky='nw', padx=20, pady=0)
        l.config(font=("Calibri", 12))
            
    def changeRunner(self, runner):
        self.id = runner['Numer']
        sex = 'Mężczyźni' if (runner['Kategoria'][0] == 'M') else 'Kobiety'
        values = ['Wszyscy', sex, runner['Kategoria']]
        self.comboBox.config(values=values)
        mode = self.combo.get()
        if mode == 'Wszyscy':
            mode = 'Wszyscy'
        elif mode in ['Kobiety', 'Mężczyźni']:
            mode = 'Kobiety' if runner['Kategoria'][0] == 'K' else 'Mężczyźni'
        else:
            mode = runner['Kategoria']
        self.combo.set(mode)
        self.refresh()
    
    def refresh(self):
        mode=self.combo.get()
        df = self.df
        runner = df[df['id'] == int(self.id)].iloc[0]
        
        if mode == 'Wszyscy':
            group = 'ALL'
            placeColumn = 'place'
        elif mode in ['Kobiety', 'Mężczyźni']:
            group = mode[0]
            placeColumn = 'place-M' if (group == 'M') else 'place-W'
        else:
            group = mode
            placeColumn = 'place-category'
        place = runner[placeColumn]
        count = self.stats[(group, 'count')]
        
        n = 20 # number of runner icons
        runnerColors = 'RRRRRXXXXXXXXXXGGGGG'
        self.canvas.delete('all')
        j = 19 - int(20 * (place-1) / (count))
        for i in range(20):
            name = 'runner'+runnerColors[i]
            self.canvas.create_image(i*30, 3, image=self.images[name], anchor=NW)
        self.canvas.create_image(j*30, 3, image=self.images['runnerB'], anchor=NW)
        self.comment1.set('Miejsce: ' + str(place) + ' / ' + str(count) + ' (' +
                        'lepiej niż ' + str(round(100*((count-place)/(count-1)), 2)) + '% wyników tej kategorii).')
        
        canvas2 = self.canvas2
        canvas2.delete('all')
        
        df2 = df if (group == 'ALL') else df[df['category'].str.contains(group, flags=re.I)]
        
        best = self.stats[(group, 'min')]
        
        for i in range(n):
            p = 1+int((count-1)*i/(n-1))
            time = df2[df2[placeColumn] < p+1]['time'].max()
            
            name = 'runner'+runnerColors[n-1-i]
            x = 570*best/time
            self.canvas2.create_image(x, 3, image=self.images[name], anchor=NW)
        x = 570*(best/runner['time'])
        self.canvas2.create_image(x, 3, image=self.images['runnerB'], anchor=NW)
        self.canvas2.create_line(0, 36, 600, 36, fill="black", width=4)
        self.comment2.set('Najlepszy czas: ' + self.strTime(best) + '. Zawodnik pokonał w tym czasie ok. ' + str((10000*best)//runner['time']) + 'm.')
        
    def comboCallback(self, *args):
        if self.df is not None:
            self.refresh()
        
    def setData(self, df, stats):
        self.df = df
        self.stats = stats
        
    def defocus(self, event):
        event.widget.master.focus_set()
        
    def loadImages(self):
        size = (35, 35)
        self.images = {}
        names = ['runnerB', 'runnerG', 'runnerR', 'runnerX']
        for name in names:
            image = Image.open('../img/'+name+'.png')
            image = image.resize(size, Image.ANTIALIAS)
            self.images[name] = ImageTk.PhotoImage(image)
            
    def strTime(self, time):
        h = time//3600
        m = time//60 - h*60
        s = time % 60
        return '' + str(h) + ':' + str(m//10) + str(m%10) + ':' + str(s//10) + str(s%10) 
        