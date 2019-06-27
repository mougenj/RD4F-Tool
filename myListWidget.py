from PyQt5 import QtCore
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListWidgetItem, QVBoxLayout, QWidget, QMenu, QMessageBox
from makeWidget import make_groupbox
from DataOfAFile import DataOfAFile


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

        self.data_from_files = []
        self.i = 0

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

    def getIndexFromName(self, name):
        start_of_name = name.split(":")[0]
        int_in_str = start_of_name.split()[1]
        index = int(int_in_str)
        return index

    def getData(self):
        if self.i != 0:
            master = self.up.get_name()
            slaves = self.down.get_names()
            index_master = self.getIndexFromName(master)
            index_slaves = [self.getIndexFromName(name) for name in slaves]

            data_master = self.data_from_files[index_master]
            data_slaves = []
            for i in index_slaves:
                data_slaves.append(self.data_from_files[i])
            return data_master, data_slaves
        return None, None
    
    def addItemFromData(self, data):
        self.data_from_files.append(data)
        if not self.up.count():
            self.up.addItemFromData(data, self.i)
        else:
            self.down.addItemFromData(data, self.i)
        self.i += 1
    
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

    def addItemFromData(self, data, i):
        i = self.int_to_str(i)
        name = data.name

        item = QListWidgetItem('Item ' + i + ": " + name)
        self.addItem(item)

    def get_names(self):
        return [self.item(i).text() for i in range(self.count())]

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
    
        # self.setStyleSheet(self.styleSheet() + """
        # QListWidget{
        #     display: none;
        # }
        # """)
    
    def get_name(self):
        return self.item(0).text()

    def addItemFromData(self, data, i):
        item = QListWidgetItem('Item ' + self.int_to_str(i) + ": " + data.name)
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