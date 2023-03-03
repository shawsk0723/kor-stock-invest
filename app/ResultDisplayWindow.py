"""
Module name
- ParkingPassbookApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""


# Import the required libraries
from tkinter import *
from tkinter import ttk

PADY = 3

class ResultDisplayWindow:

    def __init__(self, stockName="주식 분석 결과"):

        # Create an instance of tkinter frame
        win = Tk()

        win.title(f"분석 결과를 알려 드립니다~")

        # Set the size of the tkinter window
        win.geometry("700x350")

        # Create an object of Style widget
        style = ttk.Style()
        style.theme_use('clam')

        self.messageLabel = Label(win, text = stockName, height=3)
        self.messageLabel.pack(pady=PADY)

        self.setHeadRow()

        self.win = win

    def setHeadRow(self, headRow=["아이템", "밸류"]):
        treeView = ttk.Treeview(self.win, column=headRow, show='headings', height=5, padding=10)
        treeView.pack(anchor=CENTER)

        for i, head in zip(range(len(headRow)), headRow):
            treeView.column("# {}".format(i+1), anchor=CENTER)
            treeView.heading("# {}".format(i+1), text=head)

        self.treeView = treeView

    def setBodyRows(self, bodyRows):
        # Insert the data in Treeview widget
        for bodyRow in bodyRows:
            self.treeView.insert('', 'end', text="1", values=bodyRow)


    def display(self):

        self.win.mainloop()


def test():
    headRow = ["아이템", "밸류"]
    bodyRows = [['OK 세컨드', '55,000'], 
                ['페퍼스 파킹 통장', '60,000'],
                ['사이다 뱅크', '70,000'],
                ['토스 통장', '80,000'],
                ]

    resultDisplayWindow = ResultDisplayWindow('고려아연')
    resultDisplayWindow.setHeadRow()
    resultDisplayWindow.setBodyRows(bodyRows)
    resultDisplayWindow.display()

if __name__ == '__main__':
    test()