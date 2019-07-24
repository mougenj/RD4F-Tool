from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget
import DragAndDrop

class AddFiles(QWidget):
    
    def __init__(self, trigger_drag, trigger_click):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(DragAndDrop.FileEdit("Drop your files here", trigger_drag))
        boutton_ajout_fichiers = QPushButton("Add file(s)")
        boutton_ajout_fichiers.clicked.connect(trigger_click)
        self.layout.addWidget(boutton_ajout_fichiers)