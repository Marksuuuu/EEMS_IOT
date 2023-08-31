import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=1800
        height=1013
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_257=tk.Label(root)
        GLabel_257["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=18)
        GLabel_257["font"] = ft
        GLabel_257["fg"] = "#333333"
        GLabel_257["justify"] = "center"
        GLabel_257["text"] = "JOHN RAYMARK M. LLAVANES"
        GLabel_257.place(x=1390,y=10,width=400,height=75)

        GLabel_224=tk.Label(root)
        GLabel_224["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_224["font"] = ft
        GLabel_224["fg"] = "#333333"
        GLabel_224["justify"] = "center"
        GLabel_224["text"] = "label"
        GLabel_224.place(x=1270,y=10,width=109,height=75)

        GButton_213=tk.Button(root)
        GButton_213["bg"] = "#cc0000"
        ft = tkFont.Font(family='Times',size=16)
        GButton_213["font"] = ft
        GButton_213["fg"] = "#ffffff"
        GButton_213["justify"] = "center"
        GButton_213["text"] = "LOG ME OUT"
        GButton_213.place(x=1640,y=110,width=149,height=50)
        GButton_213["command"] = self.GButton_213_command

        GLabel_206=tk.Label(root)
        GLabel_206["bg"] = "#90ee90"
        ft = tkFont.Font(family='Times',size=56)
        GLabel_206["font"] = ft
        GLabel_206["fg"] = "#ffffff"
        GLabel_206["justify"] = "center"
        GLabel_206["text"] = "ONLINE"
        GLabel_206.place(x=40,y=10,width=359,height=106)

        GLabel_934=tk.Label(root)
        GLabel_934["bg"] = "#cc0000"
        ft = tkFont.Font(family='Times',size=52)
        GLabel_934["font"] = ft
        GLabel_934["fg"] = "#ffffff"
        GLabel_934["justify"] = "center"
        GLabel_934["text"] = "OFFLINE"
        GLabel_934.place(x=40,y=10,width=359,height=106)

        GLabel_897=tk.Label(root)
        GLabel_897["bg"] = "#ffb800"
        GLabel_897["cursor"] = "circle"
        ft = tkFont.Font(family='Times',size=13)
        GLabel_897["font"] = ft
        GLabel_897["fg"] = "#000000"
        GLabel_897["justify"] = "center"
        GLabel_897["text"] = "VALID TICKET AVAILABLE. ACCESS ONLY FOR CHECKING, NO TRANSACTIONS. CLOSE TO PROCEED."
        GLabel_897["relief"] = "raised"
        GLabel_897.place(x=460,y=10,width=750,height=37)

    def GButton_213_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()