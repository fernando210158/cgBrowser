from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from pandastable import Table, config
from mergeFilesP import combine_dat_files
import os
import numexpr as ne # patched to make calculate function work


def getDatFolderPath():
    folder_selected = filedialog.askdirectory()
    dFolder.set(folder_selected)

def getTrcFolderPath():
    folder_selected = filedialog.askdirectory()
    tFolder.set(folder_selected)

def getResFolderPath():
    folder_selected = filedialog.askdirectory()
    rFolder.set(folder_selected)

def aggFiles():
    if dFolder.get() == '' or rFolder.get() == '':
        messagebox.showerror('HS4CG Diag', 'Set DAT and Results Folder Paths')
        pass
    else:
        blobDat = combine_dat_files(dFolder.get(), rFolder.get(), 'dat')
        if blobDat.empty:
            messagebox.showinfo('Aggregate', f'No dat files in {dFolder.get()}')
            pass
        else:
            sessInDat = len(blobDat["sessionId"].unique())
            messagebox.showinfo('Aggregate', f'# of SessionId in dat files: {sessInDat}')
    if tFolder.get() != '':
        blobTrc = combine_dat_files(tFolder.get(), rFolder.get(), 'trc')
        if blobTrc.empty:
            messagebox.showinfo('Aggregate', f'No trc files in {tFolder.get()}')
            pass
        else:
            sessInTrc = len(blobTrc["sessionId"].unique())
            messagebox.showinfo('Aggregate', f'# of SessionId in trc files: {sessInTrc}')

def about():
    messagebox.showinfo(title='Copyrights and License',
                        message=f'nTh S.r.l. Copyright (C) V23.0\n'
                                f'This program is free sofware;\n'
                                f'you can redistribute it and/or modify it\n'
                                f'under the terms of the GNU General Public License\n'
                                f'as published by the Free Software Foundation.\n'
                                f'Using Python 3.6\n'
                                f'Pandas v.023.4\n'
                                f'matplotlib v3.0.1\n'
                                f'DataExplore library from Damien Farrell')
    return


def showRec():
    if rFolder.get() == '':
        messagebox.showerror('HS4CG Diag', 'Set Results Folder Path')
    else:
        Frame = Toplevel(root)
        Frame.geometry('1200x400')
        Frame.title('Session Records (nTh S.r.l. 2023)')

        f = Frame
        try:
            datDf = pd.read_csv(f'{rFolder.get()}/{datBlob}', sep=',', delimiter=None, na_values=[''], low_memory=False)
        except:
            messagebox.showinfo(message=f'Wrong or no {datBlob} file found at {resFolder.get()}')

        datDf = datDf.drop('Unnamed: 0', axis=1)
        sr = Table(f, dataframe=datDf, showtoolbar=True, showstatusbar=True)
        options = {'colheadercolor': 'green'}
        config.apply_options(options, sr)
        sr.show()

        def handle_left_click(event):
            #Handle left click
            rowclicked_single = sr.get_row_clicked(event)

            sessionId = datDf.iloc[rowclicked_single]['sessionId']
            nameCap = datDf.iloc[rowclicked_single]['inputFileName']
            trcDf = pd.read_csv(f'{rFolder.get()}/{trcBlob}', sep=',', delimiter=None, na_values=[''], low_memory=False)
            prSess = trcDf[trcDf['sessionId'] == sessionId]

            if prSess.empty:
                messagebox.showinfo('HS4CG Diag', 'No partial records available')
            else:
                prPress = prSess.sort_values('pWStartTime', axis=0, ascending=True)
                dropCol = ['Unnamed: 0', 'sessionId']
                prSess.drop(dropCol, axis=1, inplace=True)
                subFrame = Toplevel(root)
                subFrame.geometry('1200x400+400+300')
                subFrame.title(f'PR sessionId {sessionId}, from {nameCap}')
                pr = Table(subFrame, dataframe=prSess, showtoolbar=True, showstatusbar=True)
                options = {'colheadercolor': 'blue'}
                config.apply_options(options, pr)
                pr.show()

            def handle_left_click1(event):
                # Handle left click
                rowclicked_single1 = pr.get_row_clicked(event)
                print(rowclicked_single1)

                # Drill to the flow (selected row)
                flow = prSess.iloc[rowclicked_single1]['flow']
                flSess = prSess[prSess['flow'] == flow]
                flPress = flSess.sort_values('pWStartTime', axis=0, ascending=True)
                subFrame1 = Toplevel()
                subFrame1.geometry('1200x400+400+300')
                subFrame1.title(f'Flow {flow} of PR sessionId {sessionId}, from {nameCap}')
                fl = Table(subFrame1, dataframe=flSess, showtoolbar=True, showstatusbar=True)
                options = {'colheadercolor': 'red'}
                config.apply_options(options, fl)
                fl.show()

            pr.rowheader.bind('<Button-1>', handle_left_click1)

        sr.rowheader.bind('<Button-1>', handle_left_click)

cwd = os.getcwd()
print(cwd)
icoFile = f'{cwd}/Play.png'
trcBlob = 'blob-Trc.csv'
datBlob = 'blob-Dat.csv'
entryPathWidth = 70

root = Tk()

root.geometry('600x220')
root.title('HS4CG Browser 23.0 - nTh S.r.l. 2023')
root.resizable('True', 'True')
root.configure(background='lightgrey')
if os.path.isfile(icoFile):
    icn = PhotoImage(file=os.path.basename(icoFile))
    root.iconphoto(True, icn)

dFolder = StringVar()
datFind = Button(root, text='DAT Files Folder',command=getDatFolderPath)
datFind.grid(row=0, column=1, padx=5, pady=10, sticky='E')
datFolder = Entry(root, width=entryPathWidth, textvariable=dFolder)
datFolder.grid(row=0,column=2, padx=10)

tFolder = StringVar()
trcFind = Button(root, text='TRC Files Folder',command=getTrcFolderPath)
trcFind.grid(row=1, column=1, padx=5, pady=10, sticky='E')
trcFolder = Entry(root, width=entryPathWidth, textvariable=tFolder)
trcFolder.grid(row=1,column=2, padx=10)

rFolder = StringVar()
resFind = Button(root, text='Results Folder',command=getResFolderPath)
resFind.grid(row=2, column=1, padx=5, pady=10, sticky='E')
resFolder = Entry(root, width=entryPathWidth, textvariable=rFolder)
resFolder.grid(row=2, column=2, padx=10)

aggrBut = Button(root, text='Aggregate', command=aggFiles)
aggrBut.grid(row=3, column=1, pady=20, sticky='E')

showBut = Button(root, text='Show Records', command=showRec)
showBut.grid(row=3, column=2, padx=10, pady=20, sticky='W')

showBut = Button(root, text='About', command=about)
showBut.grid(row=3, column=2, padx=10, pady=20, sticky='E')

root.mainloop()
