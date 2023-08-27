import tkinter as tk

window = tk.Tk()
window.geometry('600x600')
window.title('HS4CG SR Browser')

def loadNextSR():
    return

def loadPrevSR():
    return

loadNextRec = tk.Button(text='Next', command=loadNextSR)
loadNextRec.grid(row=0, column=0)
loadPrevRec = tk.Button(text='Prev', command=loadPrevSR)
loadPrevRec.grid(row=0, column=1)

if __name__ == '__main__':
    window.mainloop()