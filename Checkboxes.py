from PyQt5.QtWidgets import (QGroupBox,
                             QVBoxLayout,
                             QCheckBox,
                             QScrollArea,
                             QScroller
                            )
from functools import partial
from makeWidget import make_vbox

class Checkboxes(QGroupBox):
    
    def __init__(self, name, names_of_buttons):
        super().__init__()

        self.vbox = make_vbox()
        self.names_of_buttons = names_of_buttons

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.vbox)
        QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)
        
        self.setTitle(name)
        self.setObjectName(name)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(scroll_area)
        self.checked = []
    
    def addCheckbox(self):
        i = len(self.checked)
        if i < len(self.names_of_buttons) - 1:
            cb = QCheckBox(self.names_of_buttons[i])
        else:
            cb = QCheckBox(self.names_of_buttons[-1] + str(i + 1 - (len(self.names_of_buttons)-1)))
        cb.setCheckState(True)
        cb.setTristate(False)
        self.checked.append(True)

        trigger = partial(self.state_changed, cb, i)
        cb.stateChanged.connect(trigger)
        self.vbox.layout.addWidget(cb)

    def state_changed(self, cb, i):
        self.checked[i] = cb.isChecked()
        print(self.checked)
    
    def getChecked(self):
        return self.checked

class ProfileCheckboxes(Checkboxes):

    def __init__(self, name, names_of_buttons):
        super().__init__(name, names_of_buttons)
    
    def isSourceOnly(self):
        source_only = [False] * len(self.checked)
        source_only[1] = True
        return source_only == self.checked