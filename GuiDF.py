import pandas as pd
from tkinter import *
from pandastable import Table, TableModel

pathRep = 'C:/Users/fernando/Documents/NTH/Products/CloudGaming/Training/Results'
fileName = 'blob-trc.csv'
fileName1 = 'blob-dat.csv'

class TestApp(Frame):
        """Basic test frame for the table"""
        def __init__(self, df, parent=None):
            self.parent = parent
            self.df = df
            Frame.__init__(self)
            self.main = self.master
            self.main.geometry('600x400+200+100')
            self.main.title('Table app')
            f = Frame(self.main)
            f.pack(fill=BOTH,expand=1)
            self.table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
            pt.show()
            return

df = pd.read_csv(f'{pathRep}/{fileName}', sep=',', delimiter=None, na_values=[''], low_memory=True)
df1 = pd.read_csv(f'{pathRep}/{fileName1}', sep=',', delimiter=None, na_values=[''], low_memory=True)
app = TestApp(df1)
app = TestApp(df)
#launch the app
app.mainloop()
