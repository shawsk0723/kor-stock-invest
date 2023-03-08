"""
KorDivStockAnalyzerApp

Author
- 코드장인
- https://blog.naver.com/shawgibal
"""

from tkinter import *
from tkinter import messagebox
import tkinter.ttk

import Config
import AppUtil
import ExpiryChecker
from AppLogger import LOG
from BlogOpener import openBlog
from KorDivStockAnalyzerThread import KorDivStockAnalyzerThread
from ResultDisplayWindow import ResultDisplayWindow
import UserSettings
import HelpMenu

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
        self.korDivStockAnalyzerThread = None

        self.analysisResult = False
        self.analysisFinished = False

        # output 폴더가 없다면 새로 생성
        AppUtil.makeDirIfNotExist(Config.OUR_DIR)

        self.analysisResultChecker = self.root.after(200, self.checkAnalysisResult)

    def onClosing(self):
        LOG('onClosing()')
        try:
            self.root.after_cancel(self.analysisResultChecker)
            self.root.destroy()
        except Exception as e:
            LOG(str(e))

    def start(self):

        if ExpiryChecker.checkExpiry():
            msg_box = messagebox.showerror('Error', Config.EXPIRED_MESSAGE)
            if msg_box == 'ok':
                self.root.destroy()
                return

        def startButtonCb():                            # 함수 startButtonCb() 정의
            try:
                LOG('Start Button Clicked ~')
                self.stockCode = self.codeEntry.get()
                if self.stockCode == "":
                    messagebox.showerror('Error', '코드를 입력하세요!')
                    return
                # 결과 텍스트 위젯 리셋
                self.statusText.delete(1.0,END)
                self.statusText.insert(END, '분석을 시작합니다.')
                # 분석 쓰레드 실행
                self.korDivStockAnalyzerThread = KorDivStockAnalyzerThread(self, 
                                                    UserSettings.getStockCodeList())
                self.korDivStockAnalyzerThread.start()
            except Exception as e:
                print(e)

        self.messageLabel = Label(root, text = Config.INPUT_GUIDE_LABEL, height=3)
        self.messageLabel.pack(pady=PADY)

        self.codeEntry = Entry(root, width=50)           # root라는 창에 입력창 생성
        self.codeEntry.insert(0, UserSettings.getStockCodeList()[0])
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

        self.statusText = Text(root, height=10, width=50)
        #self.statusText.insert(END, '')
        self.statusText.pack(pady=PADY*2)

        openBlogButton = Button(root, text = "코드장인의 블로그 바로가기",command=openBlog)
        openBlogButton.pack(side=BOTTOM, pady=20)

        """
        메뉴
        """
        self.menu = Menu(self.root)

        file_menu = Menu(self.menu, tearoff=0)
        file_menu.add_command(label="열기",
                              command=None
                              )
        file_menu.entryconfig(1, state=DISABLED)
        self.menu.add_cascade(label='파일', menu=file_menu)

        help_menu = Menu(self.menu, tearoff=0)
        help_menu.add_command(label="안티똥손",
                              command=HelpMenu.showAbout
                              )
        self.menu.add_cascade(label='도움말', menu=help_menu)
        self.root.config(menu=self.menu)

    def threadCb(self, success):
        self.analysisFinished = True
        self.analysisResult = success

    def checkAnalysisResult(self):
        if self.analysisFinished:
            if self.analysisResult:
                LOG('stock analysis success !')
                stockNameList = self.korDivStockAnalyzerThread.getStockName()
                resultDisplayWindow = ResultDisplayWindow(self.root, stockNameList[-1])
                analysisResult = self.korDivStockAnalyzerThread.getAnalysisResult()
                for key, value in  analysisResult.items():
                    resultDisplayWindow.setBodyRow([key, value[0]])

                self.korDivStockAnalyzerThread.saveResult()
            else:
                LOG('stock analysis fail !')

            self.analysisFinished = False

        self.analysisResultChecker = self.root.after(200, self.checkAnalysisResult)

if __name__ == "__main__":
    root = Tk()
    GUI(root).start()
    root.mainloop()    