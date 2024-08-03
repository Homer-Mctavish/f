from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from base import context
from PyQt5.QtWidgets import (QWidget, QApplication, QProgressBar, QMainWindow,QHBoxLayout, QPushButton)
from PyQt5.QtCore import (Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool)
import time
from threading import Thread


summarizer = pipeline("summarization")

def singletext(listEntry):
        #     regex=re.compile('[^a-zA-Z ]')
        #     totalbiscuit=regex.sub('',listEntry)
        whitelist=set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        totalbiscuit=''.join(filter(whitelist.__contains__, listEntry))
        tokens = sent_tokenize(totalbiscuit)
        summarized = summarizer(tokens, min_length=75, max_length=125)
        return summarized

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def run(window):
        textList=window.summarizeList
        percent = 0
        for listEntry in textList:
            if(window.is_killed==True):
                break
            else:
                output = singletext(listEntry)
                # value=output[0].keys().index("summary_text")
                value=output[0]['summary_text']
                # print(value)
                window.textBrowser.append("")
                window.textBrowser.append(''.join(value))
                percent+=1
                window.mlSummarizationStatusBar.setValue(percent)

        window.mlSummarizationStatusBar.setValue(100)
    # def run(self):
    #     """Long-running task."""
    #     for i in range(5):
    #         sleep(1)
    #         self.progress.emit(i + 1)
    #     self.finished.emit()

#possibly add a class variable to this including the summarization model so main initializes the model creation and training
class MainWindow(QMainWindow):
    def __init__(self):
        self.summarizeList = None
        self.is_paused = False
        self.is_killed = False
        self.threadpool = QThreadPool()
        super().__init__()
        # Loading the .ui file from the resources
        self.ui = uic.loadUi(context.get_resource("summarizon.ui"), self)

        # Thread for running the summary function
        # thread = Thread(target=summarymultithread(self), daemon=True)
        worker = Worker()
        self.getFileButton.clicked.connect(lambda: openFile(self))
        self.extractText.clicked.connect(lambda: textExtract(self))
        self.startSummarizing.clicked.connect(self.threadpool.start(worker))
        self.stopSummarizing.clicked.connect(lambda: kill(self))


    def openFile(window):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(window, 'Open File', ' ', 'All Files (*);;Text Files (*.txt)')
        if fileName:
            QtWidgets.QLineEdit.setText(window.lineEdit, fileName)
        return -1

    def textExtract(window):
        textlist = []
        reader = PdfReader(window.lineEdit.text())
        number_of_pages = len(reader.pages)
        complete = 0
        for page_number in range(number_of_pages):   # use xrange in Py2
            page = reader.pages[page_number]
            page_content = page.extract_text()
            #"summarize: "+page_content or page content for the nlkt version of summarize
            textlist.append(page_content)
            complete+=1
            window.progressBar.setValue(complete)
        window.progressBar.setValue(100)
        window.summarizeList = textlist
        print(window.summarizeList)



    def kill(window):
        window.is_killed=True

        # generate chunks of text \ sentences <= 1024 tokens
    def nest_sentences(document):
        nested = []
        sent = []
        length = 0
        for sentence in nltk.sent_tokenize(document):
            length += len(sentence)
            if length < 1024:
                sent.append(sentence)
            else:
                nested.append(sent)
                sent = []
                length = 0

        if sent:
            nested.append(sent)
        return nested


    def summary(window):
        textList=window.summarizeList
        percent = 0
        for listEntry in textList:
            if(window.is_killed==True):
                break
            else:
                output = singletext(listEntry)
                # value=output[0].keys().index("summary_text")
                value=output[0]['summary_text']
                # print(value)
                window.textBrowser.append("")
                window.textBrowser.append(''.join(value))
                percent+=1
                window.mlSummarizationStatusBar.setValue(percent)

        window.mlSummarizationStatusBar.setValue(100)