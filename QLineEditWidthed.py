from PyQt5.QtWidgets import QLineEdit

class QLineEditWidthed(QLineEdit):
    def __init__(self):
        super().__init()
        self.setText(text)
        self.setReadOnly(True)
        self.setObjectName(json.dumps([i, j]))
        textSize = self.fontMetrics().size(0, text)
        self.setFixedWidth(textSize.width() + 16)