import tkmacosx as tk
from tkinter import *
import numpy as np

root = Tk()
i = 0
colors = ['black', 'yellow']

B=np.array([0, 0, 0, 0, 0, 0,]*6)
C=[[0] * 10 for i in range(10) ]

def color(i) :
    A = [i]
    for t in A:
        B[t] = (B[t]+1)%2
        bts[t]['bg'] = colors[B[t]]
        bts[t]['text'] = 'YES!'



n = 36
a = 0
bts = []
for i in range(n) :
    button1 = tk.Button(root, text=i, command= lambda j = i: color(j))

    bts.append(button1)
for i in range(n) :
    bts[i].grid(row=int((i / 6) % 6), column=i % 6)

root.mainloop()