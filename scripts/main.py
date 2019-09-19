from Tkinter import *

class Application(Frame):

    def clear_text(self, *args):
        print(self.barcode_input.get())
        self.barcode_input.delete(0, 'end')

    def change_page_1(self):
        self.bg.lift()
        self.rfid_input.lift()
        self.rfid_button.lift()
        self.search_input.lift()
        self.search_button.lift()

    def change_page_2(self):
        self.bg_2.lift()
        self.barcode_input.lift()
        self.enter_button.lift()

    def createWidgets(self):

        """
        ---------------- Page 1 -----------------
        :return:
        """
        self.bg_image = PhotoImage(file='entry_p1_resized.png')
        self.bg = Label(self, image = self.bg_image)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.pack()

        self.rfid_input = Entry(self, bg = "grey")
        self.rfid_input.place(x = 250, y = 310, height = 40, width = 150)

        self.rfid_image = PhotoImage(file='rfid_icon_resized.png')
        self.rfid_button = Button(self, image = self.rfid_image, command = self.change_page_2)
        self.rfid_button.place(x = 400, y = 310, height = 40, width = 40)

        self.search_input = Entry(self, bg = "grey")
        self.search_input.place(x = 560, y = 290, height = 30, width = 130)

        self.search_image = PhotoImage(file='search_resized.png')
        self.search_button = Button(self, image=self.search_image)
        self.search_button.place(x=690, y=290, height=30, width=30)

        """
        ---------------- Page 2 -----------------
        :return: 
        """

        self.bg_image_2 = PhotoImage(file='entry_p2_resized.png')
        self.bg_2 = Label(self, image=self.bg_image_2)
        self.bg_2.place(x=0, y=0, relwidth=1, relheight=1)

        self.barcode_input = Entry(self, bg="grey")
        self.barcode_input.place(x = 550, y = 320, height = 30, width = 120)
        self.barcode_input.bind('<Return>', self.clear_text)
        self.barcode_input.focus()

        self.enter_image = PhotoImage(file='search_resized.png')
        self.enter_button = Button(self, image=self.search_image)
        self.enter_button.place(x=670, y=320, height=30, width=30)



        """
                self.QUIT = Button(self)
                self.QUIT["text"] = "QUIT"
                self.QUIT["fg"]  = "red"
                self.QUIT["command"] =  self.quit

                self.QUIT.pack({"side": "left"})

                self.hi_there = Button(self)
                self.hi_there["text"] = "Hello",
                self.hi_there["command"] = self.say_hi

                self.hi_there.pack({"side": "left"})
                """



    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.change_page_1()

root = Tk()


app = Application(master=root)

app.mainloop()
print("Testtest")
root.destroy()