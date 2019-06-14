from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QScroller

def make_vbox():
    """
        Create a QWidget, set its layout to QVBoxLayout and return it.
    """
    vbox = QWidget()
    vbox.layout = QVBoxLayout()
    vbox.setLayout(vbox.layout)
    return vbox


def make_hbox():
    """
        Create a QWidget, set its layout to QHBoxLayout and return it.
    """
    hbox = QWidget()
    hbox.layout = QHBoxLayout()
    hbox.setLayout(hbox.layout)
    return hbox


def make_scroll(scrollAreaWidgetContents):
    """
        Create a QScrollArea resizable and scrollable with the mouse, set its
        content to scrollAreaWidgetContents and return it.
    """
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(scrollAreaWidgetContents)
    QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)
    return scroll_area