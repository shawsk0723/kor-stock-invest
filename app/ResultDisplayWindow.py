"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

# Import the required libraries
from tkinter import *
from tkinter import ttk

PADY = 3

class ResultDisplayWindow(Toplevel):

    def __init__(self, root, stockName="주식 분석 결과"):

        # Create an instance of tkinter frame
        #self.win =Tk()
        super().__init__(master = root)

        self.title(f"분석 결과를 알려 드립니다~")

        # Set the size of the tkinter window
        self.geometry("700x350")

        # Create an object of Style widget
        #style = ttk.Style()
        #style.theme_use('clam')

        self.messageLabel = Label(self, text = stockName, height=3)
        self.messageLabel.pack(pady=PADY)

        self.setHeadRow()

    def setHeadRow(self, headRow=["항목", "값"]):
        treeView = ttk.Treeview(self, column=headRow, show='headings', height=8, padding=10)
        treeView.pack(anchor=CENTER)

        for i, head in zip(range(len(headRow)), headRow):
            treeView.column("# {}".format(i+1), anchor=CENTER)
            treeView.heading("# {}".format(i+1), text=head)

        self.treeView = treeView

    def setBodyRow(self, bodyRow):
        # Insert the data in Treeview widget
        self.treeView.insert('', 'end', text="1", values=bodyRow)

    def setBodyRows(self, bodyRows):
        # Insert the data in Treeview widget
        for bodyRow in bodyRows:
            self.setBodyRow(bodyRow)

    def display(self):
        #self.mainloop()
        pass



def test():
    headRow = ["아이템", "밸류"]
    bodyRows = [['OK 세컨드', '55,000'], 
                ['페퍼스 파킹 통장', '60,000'],
                ['사이다 뱅크', '70,000'],
                ['토스 통장', '80,000'],
                ]

    resultDisplayWindow = ResultDisplayWindow('고려아연')
    #resultDisplayWindow.setHeadRow()
    resultDisplayWindow.setBodyRows(bodyRows)
    resultDisplayWindow.display()

if __name__ == '__main__':
    test()