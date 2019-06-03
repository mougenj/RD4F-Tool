# todo: remove them
from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout, 
                             QTabWidget,
                             QDesktopWidget,
                             QMainWindow,
                             QAction,
                             QMenuBar,
                             QDialog,
                             QMessageBox,
                             QHBoxLayout,
                             QLabel
                            )
from PyQt5.QtGui import QIcon, QColor, QPalette, QBrush, QPixmap, QFont
import matplotlib.pyplot as plt
from FirstTab import FirstTab
from SecondTab import SecondTab
from ThirdTab import ThirdTab
import os
from PyQt5.QtCore import Qt



class AboutWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.title = 'RDRP Database Tools - About'
        self.left = 10
        self.top = 10
        self.width = 640  # 640
        self.height = 320
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + "ressources" +  os.path.sep + "logo.png"))
        self.center()
        self.initUI()

    def center(self):
        # see answer of BPL on https://stackoverflow.com/questions/39046059/pyqt-location-of-the-window
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        maxX = ag.width() - widget.width()
        maxY = 2 * ag.height() - sg.height() - widget.height()
        self.move(maxX/2, maxY/2)

    def make_pixmap(self, picture_name):
        label = QLabel()
        label.setObjectName(picture_name)
        pixmap = QPixmap(picture_name)
        label.setPixmap(pixmap)
        return label

    def initUI(self):
        central_widget = QWidget()

        central_widget.layout = QHBoxLayout()
        central_widget.setLayout(central_widget.layout)
        logo = self.make_pixmap("ressources/lspm-trasparent.png")
        central_widget.layout.addWidget(logo)

        text_area = make_vbox()
        # todo: demander une confirmation de la traduction
        description = """
        <html>
        <h1>RDRP Database Tools</h1>
        <h3>"Reaction-Diffusion modelling for Retention and Permation Database Tools"</h3>
        <p><b>Version 1.0</b></p>
        <br/>
        <p> Graphical User Interface made by the <a href=\"www.lspm.cnrs.fr/\">LSPM</a> (Laboratory of Sceinces of Processes and Materials).</p>
        </html>"""
        desc_label = QLabel(description)
        desc_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        desc_label.setOpenExternalLinks(True)
        text_area.layout.addWidget(desc_label)
        central_widget.layout.addWidget(text_area)
        p = central_widget.palette()
        p.setColor(central_widget.backgroundRole(), QColor(0, 0, 0))
        central_widget.setPalette(p)
        self.setCentralWidget(central_widget)

def make_vbox():
    vbox = QWidget()
    vbox.layout = QVBoxLayout()
    vbox.setLayout(vbox.layout)
    return vbox


def make_hbox():
    hbox = QWidget()
    hbox.layout = QHBoxLayout()
    hbox.setLayout(hbox.layout)
    return hbox

