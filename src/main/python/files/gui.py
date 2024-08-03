from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from base import context
from logic import openFile, textExtract, summary, kill
from PyQt5.QtWidgets import (QWidget, QApplication, QProgressBar, QMainWindow,QHBoxLayout, QPushButton)
from PyQt5.QtCore import (Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool)
import time
from threading import Thread

class Worker(QRunnable):
    '''
    Worker thread
    '''

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        print("Thread start")
        summary(self)
        print("Thread complete")

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
