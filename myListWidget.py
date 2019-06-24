from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem, QVBoxLayout, QWidget, QMenu
from makeWidget import make_groupbox

class DoubleThumbListWidget(QWidget):
    """
        A Qwidget that contains a ThumbListWidget and a UniqueThumbListWidget.
        It xill link them and display the  UniqueThumbListWidget above the
        ThumbListWidget.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.down = ThumbListWidget()
        self.up = UniqueThumbListWidget(self.down)

        self.up.setMinimumSize(20, 20)
        self.up.setMaximumHeight(20)
        gb_up = make_groupbox("Fichier principal", self.up)
        gb_up.setMaximumHeight(80)

        self.down.setMinimumSize(100, 100)
        gb_down = make_groupbox("Fichiers secondaires", self.down)
        gb_down.setMinimumSize(self.down.width(), 400)

        self.layout.addWidget(gb_up)
        self.layout.addWidget(gb_down)
    
    def addItemFromName(self, name):
        if not self.up.count():
            self.up.addItemFromName(name)
        else:
            self.down.addItemFromName(name)

class ThumbListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(False)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)
    
    def setUniqueList(self, uniqueList):
        pass

    def addItemFromName(self, name):
        item = QListWidgetItem('Item ' + self.int_to_str(self.count()) + name)
        self.addItem(item)

    def int_to_str(self, x):
        s = str(x)
        while(len(s)) < 3:
            s = "0" + s
        return s

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(ThumbListWidget, self).dragEnterEvent(event)
    
    """
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(ThumbListWidget, self).dragMoveEvent(event)
    
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            # links = []
            # for url in event.mimeData().urls():
            #     links.append(str(url.toLocalFile()))
            #self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.setDropAction(QtCore.Qt.MoveAction)
            super(ThumbListWidget, self).dropEvent(event)
    """
    
    def removeElementFromText(self, text):
        supression_index = -1
        for i in range(self.count()):
            if self.item(i).text() == text:
                supression_index = i
        if supression_index >= 0:
            item = self.item(supression_index)
            self.takeItem(supression_index)
        
    def sort(self):
        def getIndexFromText(element):
            text = element.text()
        self.previous_state = []
        for i in range(self.count()):
            self.previous_state.append(self.item(i).clone())
        self.previous_state.sort(key=lambda x : x.text())
        self.clear()
        for element in self.previous_state:
            self.addItem(element.clone())

    def openMenu(self, event):
            contextMenu = QMenu(self)
            #newItems = contextMenu.addAction("Open Files")
            removeItems = contextMenu.addAction("Remove Files")
            action = contextMenu.exec_(self.mapToGlobal(event))
            #if action == newItems:  # todo
            #    print("TODO")
            if action == removeItems:
                indexes = [item.row() for item in self.selectedIndexes()]
                for index in indexes:
                    self.takeItem(index)


class UniqueThumbListWidget(QListWidget):
    def __init__(self, other, parent=None):
        super().__init__(parent)
        self.other = other
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.previous_state = []

        self.other.setUniqueList(self)
        # self.setStyleSheet(self.styleSheet() + """
        # QListWidget{
        #     display: none;
        # }
        # """)

    def addItemFromName(self, name):
        item = QListWidgetItem('Item ' + self.int_to_str(self.count()) + name)
        self.addItem(item)

    def int_to_str(self, x):
        s = str(x)
        while(len(s)) < 3:
            s = "0" + s
        return s
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(UniqueThumbListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(UniqueThumbListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        # self.clear()
        self.other.removeElementFromText("a")
        if event.mimeData().hasUrls():
            
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            
            # links = []
            # for url in event.mimeData().urls():
            #     links.append(str(url.toLocalFile()))
            #self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            self.previous_state = []
            for i in range(self.count()):
                self.previous_state.append(self.item(i).clone())
            self.clear()
            event.setDropAction(QtCore.Qt.MoveAction)
            super(UniqueThumbListWidget, self).dropEvent(event)
            if self.count() > 1:
                self.clear()
                for element in self.previous_state:
                    self.addItem(element.clone())
            elif self.previous_state:
                self.other.removeElementFromText(self.item(0).text())
                self.other.addItem(self.previous_state[0])
                self.other.sort()