import queue
from threading import Thread
import pyttsx3
from tkinter import *
from tkinter import messagebox

START_MESSSAGE = "안티똥손을 시작합니다."
STOP_MESSAGE = '안티똥손을 종료합니다.'

# Speaker Thread
class Speaker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.queue = queue.Queue()
        self.daemon = True
        self.isRunning = False
        self.start()
        self.say(START_MESSSAGE)

    def run(self):
        print('speaker thread starts~')
        self.isRunning = True
        tts_engine = pyttsx3.init()

        while self.isRunning:
            print(f'wait for message~')
            message = self.queue.get(block=True, timeout=None)
            print(f'message = {message}')
            tts_engine.say(message)
            tts_engine.runAndWait()
            if message == STOP_MESSAGE:
                break

        print('speaker thread stops~')

    def say(self, message):
        self.queue.put_nowait(message)

    def stopRequest(self):
        self.queue.put_nowait(STOP_MESSAGE)


if __name__ == '__main__':
    root = Tk()
 
    # 버튼 클릭 이벤트 핸들러
    def okClick():
        message = txt.get()
        speaker.say(message)

    def destroyClick():
        speaker.stopRequest()
        speaker.join()
        root.destroy()


    lbl = Label(root, text="스피커")
    #lbl.grid(row=0, column=0)
    lbl.pack()
    txt = Entry(root)
    txt.insert(0, '안녕하세요?')
    txt.pack()
    
    # 버튼 클릭 이벤트와 핸들러 정의
    btnSay = Button(root, text="Say", command=okClick)
    #btn.grid(row=1, column=1)
    btnSay.pack()
    
    btnDestroy = Button(root, text="Finish", command=destroyClick)
    btnDestroy.pack()


    speaker = Speaker()
    #speaker.say(start_message)

    root.mainloop()
