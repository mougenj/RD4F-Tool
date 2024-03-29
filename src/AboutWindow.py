from PyQt5.QtWidgets import (QWidget,
                             QDesktopWidget,
                             QMainWindow,
                             QHBoxLayout,
                             QLabel
                            )
from PyQt5.QtGui import QIcon, QColor, QPixmap 
import matplotlib.pyplot as plt
import os
from PyQt5.QtCore import Qt
import makeWidget


class AboutWindow(QMainWindow):
    """
        A window designed to contain informations about the application.
    """
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
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + "ressources" +  os.path.sep + "2.png"))
        self.center()
        self.initUI()

    def center(self):
        """
            Center the window in the middle of the screen.
        """
        # see answer of BPL on https://stackoverflow.com/questions/39046059/pyqt-location-of-the-window
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        maxX = ag.width() - widget.width()
        maxY = 2 * ag.height() - sg.height() - widget.height()
        self.move(maxX/2, maxY/2)

    def initUI(self):
        """
            Create the GUI of the window.
        """
        central_widget = QWidget()

        central_widget.layout = QHBoxLayout()
        central_widget.setLayout(central_widget.layout)
        logo = makeWidget.make_pixmap("ressources/logo2.png")
        central_widget.layout.addWidget(logo)

        text_area = makeWidget.make_vbox()
        # todo: demander une confirmation de la traduction
        description = """
        <html>
        <h1>RDRP Database Tools</h1>
        <h3>"Reaction-Diffusion modelling for Retention and Permation Database Tools"</h3>
        <p><b>Version 1.0</b></p>
        <br/>
        <p> A Graphical User Interface made by the <a href="www.lspm.cnrs.fr/">LSPM</a> (Laboratory of Sciences of Processes and Materials).</p>
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



