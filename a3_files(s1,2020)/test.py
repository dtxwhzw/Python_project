from tkinter import*
import tkinter.font as tkFont
import tkmacosx
# #初始化Tk()
# myWindow = Tk()
# #设置标题
# myWindow.title('Python GUI Learning')
# myWindow.config(bg='black')
#
# #创建一个标签，显示文本
# Label(myWindow, text="user-name",bg='red',font=('Arial 12 bold'),width=95,height=20).pack(pady = 1)
# Label(myWindow, text="password",bg='green',width=20,height=5).pack()
# #进入消息循环
# myWindow.geometry('600x600+500+200')
# myWindow.mainloop()
e1 = []

root = Tk()
colcut = 10
color = 'green'
root.config(bg = 'black')
root.geometry('+500+200')
ft = tkFont.Font(family='Fixdsys', size=12, weight=tkFont.BOLD)
Label(root,text = 'Pokemon: Got 2 Fins Them All!',fg = 'white',bg = '#F08080',height = 3,font =ft).grid(row = 0,sticky = W+E,columnspan=10)
for j in range(10):
    for i in range(10):

        e1[j][i] = tkmacosx.Button(height=60, width=60, background = '#228B22',command = press(j,i))
        e1[j][i].grid(row=j+2,column=i, sticky=W+E+N+S,padx = 1,pady=1)
        #Label( bg=color).grid(row=j,column=i, sticky=W+E+N+S,padx = 1,pady=1)
        #Label(text=color, bg=color).pack(side = TOP,expand = False,fill =BOTH,padx=1,pady=1)
def press(j,i):
    e1[j][i]['bg'] = 'red'

#e2 = Label(text = 'Hello',fg = 'white',bg = 'red')
root.mainloop()