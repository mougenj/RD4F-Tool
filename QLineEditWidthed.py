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
        self.setReadOnly(not editable)
        textSize = self.fontMetrics().size(0, "")
        self.editingFinished.connect(sayCoucou)
        if text_to_be_able_to_display:
            textSize = self.fontMetrics().size(0, text_to_be_able_to_display)
        tempSize = self.fontMetrics().size(0, text)
        if tempSize.width() > textSize.width():
            textSize = tempSize
        self.setFixedWidth(textSize.width() + 16)
        
def sayCoucou():
    print("coucou (edition terminee)")