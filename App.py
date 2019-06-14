from PyQt5.QtWidgets import (QDesktopWidget,
                             QMainWindow,
                             QAction,
                             QMenuBar
                            )
from PyQt5.QtGui import QIcon, QColor
import os
from PyQt5.QtCore import Qt
from HelpWindow import HelpWindow
from MainWidget import MainWidget
from AboutWindow import AboutWindow


class App(QMainWindow):
    """
        Main class of the application.
        It display a MainWidget, wich contains infos on data included in a
        JSON file. To get more informations about this MainWidget, please read
        the documentation of the class MainWidget in the file MainWidget.py.
        It also display a menu (which can be used to show a Help window and a
        window about the author of this program).
    """
    def __init__(self):
        """
            Init the App by setting its title, its icon, its background color
            and creating its menu and a MainWidget.
        """
        super().__init__()
        self.title = 'RDRP Database Tools'
        self.left = 10
        self.top = 10
        self.width = 1600  # 640
        self.height = 640
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + "ressources" +  os.path.sep + "logo.png"))
        # menu part
        bar = self.menuBar()
        barp = bar.palette()
        # import pdb; import rlcompleter; pdb.Pdb.complete=rlcompleter.Completer(locals()).complete; pdb.set_trace()
        color = barp.text().color()
        txtcolor = "rgb(" + str(color.red()) + ", " + str(color.green()) + ", " + str(color.blue()) + ")"
        color = barp.button().color()

        list_color = [color.red(), color.green(), color.blue()]
        backcolor = "rgb("
        backcolor += ", ".join([str(c) for c in list_color])
        backcolor += ")"

        backcolor_darker = "rgb("
        backcolor_darker += ", ".join([str(int(c*9/10)) for c in list_color])
        backcolor_darker += ")"

        self.setStyleSheet("""
        QMenuBar {
            background-color: """ + backcolor + """ ;
            color: """ + txtcolor + """;
        }

        QTreeWidget {
            background-color: """ + backcolor + """ ;
            color: """ + txtcolor + """;
        }

        QMenuBar::item {
            background-color: """ + backcolor + """ ;
            color: """ + txtcolor + """;
        }

        QMenuBar::item::selected {
            background-color: """ + backcolor_darker + """;
        }

        QMenu {
            background-color: """ + backcolor + """ ;
            color: """ + txtcolor + """;         
        }

        QMenu::item::selected {
            background-color: """ + backcolor_darker + """;
        }
    """)
        
        helpAction = QAction('Show help', self)
        helpAction.setShortcut('Ctrl+H')
        # helpAction.setStatusTip('Open Directory')
        helpAction.triggered.connect(self.openHelp)
        aboutAction = QAction("Show about", self)
        aboutAction.setShortcut("Ctrl+A")
        aboutAction.triggered.connect(self.openAbout)
        helpMenu = bar.addMenu('Help')
        helpMenu.addAction(helpAction)
        aboutMenu = bar.addMenu('About')
        aboutMenu.addAction(aboutAction)
        self.setCentralWidget(MainWidget())
        self.center()
        #set background color
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(0, 113, 134))
        self.setPalette(p)

        barp.setColor(bar.backgroundRole(), color)
        bar.setPalette(barp)
        color = barp.button().color()
        self.show()

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

    def openHelp(self):
        """
            Open the Help window.
        """
        dialog = HelpWindow(self)
        dialog.show()
    
    def openAbout(self):
        """
            Open a window that display informations about the author of this
            application.
        """
        dialog = AboutWindow(self)
        dialog.show()
