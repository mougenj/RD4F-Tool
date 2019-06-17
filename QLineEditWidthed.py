from PyQt5.QtWidgets import QLineEdit

class QLineEditWidthed(QLineEdit):
    """
        Create a special QLineEdit that adapt to its content and wich can be
        editable or not.
        If text_to_be_able_to_display is passed, it will take the maximum size
        ('text' vs 'text_to_be_able_to_display')
    """
    def __init__(self, text, editable=False, text_to_be_able_to_display=None):
        super().__init__()
        self.setText(text)
        self.editable = editable
        self.setReadOnly(not editable)
        textSize = self.fontMetrics().size(0, "")
        
        if text_to_be_able_to_display:
            textSize = self.fontMetrics().size(0, text_to_be_able_to_display)
        tempSize = self.fontMetrics().size(0, text)
        if tempSize.width() > textSize.width():
            textSize = tempSize
        self.setFixedWidth(textSize.width() + 16)
    
    def autoUpdate(self):
        try:
            if self.other.editable:
                number = float(self.text()) * self.coef
                self.other.setText("{:.2e}".format(number))
        except Exception as e:
            self.other.setText("")

    def setAutoUpdate(self, other, coef):
        self.other = other
        self.coef = coef
        self.editingFinished.connect(self.autoUpdate)