from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QScroller, QLabel, QGroupBox
from PyQt5.QtGui import QPixmap 

def make_vbox(*args):
    """
        Create a QWidget, set its layout to QVBoxLayout and return it.
    """
    vbox = QWidget()
    vbox.layout = QVBoxLayout()
    vbox.setLayout(vbox.layout)
    if args:
        for arg in args:
            vbox.layout.addWidget(arg)
    return vbox


def make_hbox(*args):
    """
        Create a QWidget, set its layout to QHBoxLayout and return it.
    """
    hbox = QWidget()
    hbox.layout = QHBoxLayout()
    hbox.setLayout(hbox.layout)
    if args:
        for arg in args:
            hbox.layout.addWidget(arg)
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

def make_pixmap(picture_name):
    """
        Create a QLabel with the name picture_name, containing a QPixmap
        made from the image picture_name. 
    """
    label = QLabel()
    label.setObjectName(picture_name)
    pixmap = QPixmap(picture_name)
    label.setPixmap(pixmap)
    return label

def make_groupbox(name, *args):
    gb_material = QGroupBox()
    gb_material.layout = QVBoxLayout()
    gb_material.setLayout(gb_material.layout)
    gb_material.setTitle(name)
    gb_material.setObjectName(name)
    if args:
        for arg in args:
            gb_material.layout.addWidget(arg)
    return gb_material
    