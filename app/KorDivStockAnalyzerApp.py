"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""



import traceback
from tkinter import *
from tkinter import messagebox
import tkinter.ttk

import Config
from AppLogger import LOG
from BlogOpener import openBlog
from KorDivStockAnalyzerThread import KorDivStockAnalyzerThread
import ExpiryChecker

"""
App config
"""

WIN_SIZE = Config.WIN_SIZE
WIN_TITLE = Config.WIN_TITLE
WIN_FONT = "*Font"
WIN_FONT_SETTING = "맑은고딕 15"
PADY = 5

"""
GUI Class
"""
class GUI:

    def __init__(self, root):
        self.root = root
        root.geometry(WIN_SIZE)                 # 창 크기설정
        root.title(WIN_TITLE)           # 창 제목설정
        root.option_add(WIN_FONT, WIN_FONT_SETTING)    # 폰트설정
        root.resizable(False, False)             # x, y 창 크기 변경 불가
        root.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.stockCode = ""
        self.rorDivStockAnalyzerThread = None

        self.analysisResult = False
        self.analysisFinished = False
        #self.downloadWorker = DownloadWorker(os.getcwd() + '\\download\\', self._callback)
        #self.downloadWorker.start()
        self.analysisResultChecker = self.root.after(200, self.checkAnalysisResult)

    def onClosing(self):
        LOG('onClosing()')
        try:
            root.after_cancel(self.analysisResultChecker)
            root.destroy()
        except Exception as e:
            LOG(str(e))

    def start(self):

        if ExpiryChecker.checkExpiry():
            msg_box = messagebox.showerror('Error', '만료되었습니다!')
            if msg_box == 'ok':
                root.destroy()
                return

        def startButtonCb():                            # 함수 startButtonCb() 정의
            try:
                LOG('Start Button Clicked ~')
                self.stockCode = self.codeEntry.get()
                if self.stockCode == "":
                    messagebox.showerror('Error', '코드를 입력하세요!')
                    return
                # 결과 리셋
                self.resultText.delete(1.0,END)
                self.resultText.insert(END, '분석 결과')
                # 분석 쓰레드 실행
                self.rorDivStockAnalyzerThread = KorDivStockAnalyzerThread(self)
                self.rorDivStockAnalyzerThread.start()
            except Exception as e:
                print(e)

        self.messageLabel = Label(root, text = '주식 코드 입력', height=3)
        self.messageLabel.pack(pady=PADY)

        self.codeEntry = Entry(root, width=50)           # root라는 창에 입력창 생성
        self.codeEntry.pack(pady=PADY)                               # 입력창 배치

        self.startButton = Button(root)                       # root라는 창에 버튼 생성
        self.startButton.config(text= Config.START_BUTTON_LABEL)               # 버튼 내용 
        self.startButton.config(width=20)                      # 버튼 크기
        self.startButton.config(command=startButtonCb)               # 버튼 기능 (btnpree() 함수 호출)
        self.startButton.pack(pady=PADY*2)                                 # 버튼 배치

        self.progressbar=tkinter.ttk.Progressbar(root, maximum=100, mode="indeterminate")
        self.progressbar.pack(pady=PADY)

        self.statusLabel = Label(root, text = f'진행 상태')
        self.statusLabel.pack(pady=PADY*2)

        #self.resultLabel = Label(root, text = f'분석 결과')
        self.resultText = Text(root, height=10, width=50)
        self.resultText.insert(END, '분석 결과')
        self.resultText.pack(pady=PADY*2)

        openBlogButton = Button(root, text = "코드장인의 블로그 바로가기",command=openBlog)
        openBlogButton.pack(side=BOTTOM, pady=20)

    def threadCb(self, success):
        self.analysisFinished = True
        self.analysisResult = success

    def checkAnalysisResult(self):
        if self.analysisFinished:
            if self.analysisResult:
                LOG('stock analysis success !')
                stockAnalyzer = self.rorDivStockAnalyzerThread.stockPricer
                stockAnalyzer.savePriceDivChart()
                stockName = stockAnalyzer.getStockName()
                analysisResult = stockAnalyzer.getResult()
                analysisResultTxt = f"{stockName} 분석 결과"
                for key, value in analysisResult.items():
                    analysisResultTxt += '\n'
                    analysisResultTxt += f'{key}: {value}'

                self.resultText.delete(1.0,END) # 텍스트 위젯 리셋
                self.resultText.insert(END, analysisResultTxt)
            else:
                LOG('stock analysis fail !')

            self.analysisFinished = False

        self.analysisResultChecker = self.root.after(200, self.checkAnalysisResult)

if __name__ == "__main__":
    root = Tk()
    GUI(root).start()
    root.mainloop()    