from xt import *
from ui.ui_dl_add import *
import requests, sys, concurrent.futures,time, os, re, platform
DL_CUSTOM_TITLE_BAR=True

class Addfxns(QDialog):
    def __init__(self,myparent):
        QDialog.__init__(self)
        self.dialogUI = Ui_Addbox()
        self.dialogUI.setupUi(self)
        self.myparent=myparent
        self.link=''
        self.dialogUI.pushButton.clicked.connect(lambda: self.close())
        self.dialogUI.cancelbtn.clicked.connect(self.close)
        self.dialogUI.addbtn.clicked.connect(self.addclicked)
        self.dialogUI.urlbox.textChanged.connect(self.on_lineedit)
        self.dialogUI.addbtn.setEnabled(False)
        self.dialogUI.analysebtn.hide()
        # self.dialogUI.filename.hide()
        # self.dialogUI.flenlabel.hide()

        if DL_CUSTOM_TITLE_BAR:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            def moveWindow(event):
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
                    self.dragPos = event.globalPosition().toPoint()
                    event.accept()
            self.dialogUI.titleframe.mouseMoveEvent = moveWindow
        # self.setWindowModality(Qt.ApplicationModal)
        # self.dialogUI.urlbox.setStyleSheet(u"background-color: rgb(9,11,16);")
        # self.shadow = QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(17)
        # self.shadow.setXOffset(0)
        # self.shadow.setYOffset(0)
        # self.shadow.setColor(QColor(0, 0, 0, 150))
        # self.dialogUI.setGraphicsEffect(self.shadow)
        self.show()

    def mousePressEvent(self, event):
        # self.dragPos = event.globalPos() # Deprecated function
        p = event.globalPosition()
        self.dragPos = p.toPoint()

    def on_lineedit(self):
        if not self.validateUrl(self.dialogUI.urlbox.text()):
            self.dialogUI.warning.setText("Invalid URL syntax")
            self.dialogUI.addbtn.setEnabled(False)
        else:
            # self.dialogUI.warning.setText("Analysing URL")
            # self.checkurl(self.dialogUI.urlbox.text())
            self.dialogUI.warning.setText("OK")            
            self.dialogUI.addbtn.setEnabled(True)


    def validateUrl(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, str(url))
    
    def addclicked(self):
        self.myparent.add(self.dialogUI.urlbox.text())
        self.close()

    def checkurl(self,url):
        try:
            r=requests.head(url)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
        else:
            # print(r.headers)
            if 'Location' in r.headers.keys():
                self.checkurl(r.headers['Location'])
            # print(r.headers['Location'])
            else:
                # print(r.url,r.headers['content-length'])
                self.link=str(r.url)
                self.dialogUI.flenlabel.setText(str(r.headers['content-length']))
                self.setfilename()

    def setfilename(self):
        temp=self.link.split("/")[-1]
        if len(temp)>100:
            temp=temp[:100]
        temp=temp.split("?")[0]
        self.dialogUI.filename.setText(temp)