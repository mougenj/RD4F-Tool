from PyQt5.QtWidgets import (QDesktopWidget,
                             QMainWindow,
                             QLabel
                            )
from PyQt5.QtGui import QIcon, QColor
import os
from PyQt5.QtCore import Qt
import makeWidget


class HelpWindow(QMainWindow):
    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent)
        self.title = 'RDRP Database Tools - Help'
        self.left = 10
        self.top = 10
        self.width = 840  # 640
        self.height = 700
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + "ressources" +  os.path.sep + "logo.png"))
        self.initUI()
        self.center()

    def center(self):
        # see answer of BPL on https://stackoverflow.com/questions/39046059/pyqt-location-of-the-window
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        maxX = ag.width() - widget.width()
        maxY = 2 * ag.height() - sg.height() - widget.height()
        self.move(maxX/2, maxY/2)
    
    def initUI(self):
        central_widget = makeWidget.make_vbox()
        central_widget.setLayout(central_widget.layout)

        text_area = makeWidget.make_vbox()
        # todo: demander une confirmation de la traduction
        description = """
        <html>
        <h1>RDRP Database Tools - Help</h1>
        <p>This GUI is meant to help manipulating a standardized format for chemical reactions.</p>

        <h3>Read</h3>
        <p>This application have two main tabs: "Read" and "Write". The first one allows you to read datas from a JSON file, while the second let you create your own JSON file by filling forms. To add a file to read, use one of these two buttons:</p>
        <br/><img src="ressources/addFiles.png"></img><br/>
        <p>You can drop files on the left part to open them or you can click on the right button to open a new window in which you can choose some files to open.</p>
        <br/><img src="ressources/addMultpleFiles.png"></img><br/>
        <p><div style="color: #FF0000;text-decoration: underline;">Tips:</div> you can hold ctrl and click on as many files as you want to open them all.</p>
        <p>Once files are opened, you can see what is inside by click on the corresponding tab. The corresponding informations will be printed on the left.</p>
        <br/><img src="ressources/infosOnFiles.png"></img><br/>
        <p>If you click on one of the coefficient buttons, the graphs on the right will be updated with the values inside the opened files. For instance, if you click on "Diffusion", the program will search every "diffusion" part in every opened file and will plot it in the graph.</p>
        <br/><img src="ressources/drawCoefficients.png"></img><br/>
        <br/><img src="ressources/drawnCoefficients.png"></img><br/>
        <p>You can modify the graph with the below buttons:</p>
        <br/><img src="ressources/modifyGraph.png"></img><br/>
        <li>
            <ul>You can move in the graph by clicking on the arrows and then by clicking on the graph, holding the mouse button pressed and dragging the mouse.</ul>
            <ul>After a click on the magnifying glass, you can zoom in the graph.</ul>
            <ul>The third button let you modify the height and the weight of the graph.</ul>
            <ul>The fourth button let you add a title to the graph, edit its axis, change the legend... It can be usefull to get a better looking graph.
            <br/>
            <div style="color: #FF0000;text-decoration: underline;">Be careful:</div> if you draw a graph using one of the coefficient buttons (on the left of the graph), these changes will be lost. Be sure to export your graph before drawing another one.</ul>
            <ul>The floppy icon let you export the graph into an image (ie: save it on your computer)</ul>
        </li>

        <h3>Write</h3>
        <p></p>
        <br/>
        </html>"""
        desc_label = QLabel(description)
        desc_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        desc_label.setOpenExternalLinks(True)
        desc_label.setWordWrap(True)
        scroll = makeWidget.make_scroll(desc_label)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        central_widget.layout.addWidget(scroll)
        p = central_widget.palette()
        p.setColor(central_widget.backgroundRole(), QColor(0, 0, 0))
        central_widget.setPalette(p)
        self.setCentralWidget(central_widget)