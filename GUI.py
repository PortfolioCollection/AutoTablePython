from tkinter import Tk, Label, Button
from tkinter import W

class MyFirstGUI:
    def __init__(self,timeslots,name,master):
        self.master = master
        master.title("Autotable")
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
        button = Button(master, text=name, width = 32,state="disabled")
        button.grid(row=0, column=0)

        #timeslots = [[(0,3)],[(0,5),(6,7)],[(1,2),(2,3),(3,5)],[(1,4),(6,9)],[(0,10)]]
        
        for i in range(1,15):
            if 8+i > 12:
                num = i-4
            else:
                num = 8+i
            button = Button(master, text=str(num), width = 32,state="disabled")
            button.grid(row=i, column=0)
        for i in range(5):
            button = Button(master, text=days[i], width = 32,state="disabled")
            button.grid(row=0, column=i+1)

        
        for i in range(1,6):
            x = 0
            j = 1
            while j < 15:
                button = Button(master, text="", width = 32, command=lambda: print("blank"))
                if x < len(timeslots[i-1]) and timeslots[i-1][x].start-9 == j-1:
                    span = int(timeslots[i-1][x].end-timeslots[i-1][x].start)
                    name = timeslots[i-1][x].name
                    button = Button(master, text=name,anchor="nw", bg='#40E0D0',
                                    width = 32, command=lambda save=name: print(save),font=('helvetica', 4))
                    button.grid(row=j, column=i, rowspan = span,sticky="nsew")
                    for s in range(span):
                        j+=1
                    j-=1
                    x+=1
                else:
                    button.grid(row=j, column=i,sticky="nsew")
                j+=1

if __name__ == "__main__":
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()
