from pandastable import Table, TableModel
import tkinter as tk
import pandas as pd

pathTrc = 'C:/Users/Utente/Documents/HS4CG/TRC'
pathDat = 'C:/Users/Utente/Documents/HS4CG'
pathRep = 'C:/Users/Utente/Documents/HS4CG/Results'
trcBlob = 'blob-trc.csv'
datBlob = 'blob-dat.csv'

df = pd.read_csv(f'{pathRep}/{datBlob}', sep=',', delimiter=None, na_values=[''], low_memory=True)
trcDf = pd.read_csv(f'{pathRep}/{trcBlob}', sep=',', delimiter=None, na_values=[''], low_memory=True)

app = tk.Toplevel()

app.title('Table app')
f = tk.Frame(app)
f.pack()

table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)

pt.show()

def handle_left_click(event):
    """Handle left click"""
    rowclicked_single = table.get_row_clicked(event)
    print(rowclicked_single)
    table.setSelectedRow(rowclicked_single)
    table.redraw()
    print(df.loc[rowclicked_single]['sessionId'])
pt.rowheader.bind('<Button-1>',handle_left_click)




app.mainloop()