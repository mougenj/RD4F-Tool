import sip
sip.setdestroyonexit(True)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPushButton,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout, 
                             QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap
import sys


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Titre'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        tabs = QTabWidget()
        tabs.resize(self.width, self.height)
        tabs.addTab(self.create_fisrt_tab(), "Tab 1")
        tabs.addTab(self.create_second_tab(), "Tab 2")
        tabs.addTab(self.create_third_tab(), "Tab 3")

        layout = QVBoxLayout()  # contient les tabs
        layout.addWidget(tabs)
        self.setLayout(layout)

        #self.resize(pixmap.width()+self.width,pixmap.height()+self.height)
        self.show()
    
    def create_fisrt_tab(self):
        # create the tab
        tab1 = QWidget()
        tab1.layout = QHBoxLayout()
        tab1.setLayout(tab1.layout)
        # fill it
        label = QLabel(self)
        pixmap = QPixmap('image.png')
        label.setPixmap(pixmap)
        tab1.layout.addWidget(label)
        #return it
        return tab1
    
    def create_second_tab(self):
        # create the tab
        tab2 = QWidget()
        tab2.layout = QHBoxLayout()
        tab2.setLayout(tab2.layout)
        # fill it
        boutton = QPushButton("PyQt5 button")
        tab2.layout.addWidget(boutton)
        # return it
        return tab2
    
    def create_third_tab(self):
        # create the tab
        tab3 = QWidget()
        tab3.layout = QVBoxLayout()
        tab3.setLayout(tab3.layout)
        # return it
        return tab3




# def main(args):
#     app = QApplication(args)
#     widget = QWidget(None)
#     widget.resize(400,90)
#     button = QPushButton("Hello World !", widget)
#     button.resize(100,30)
#     widget.show()
#     app.exec_()
# if __name__ == "__main__":
#     main(sys.argv)



if __name__ == '__main__':
    print("création de l'interface")
    #print(sys.argv)
    app = QApplication(sys.argv)
    print("lancement de l'interface")
    ex = App()
    print("sortie de l'interface")
    rc = app.exec_()
    print("sortie prog")
    del app
    sys.exit(rc)
