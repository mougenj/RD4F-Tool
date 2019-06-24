from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout
                            )
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class PltWindow(QWidget):
    """
        This widget act as a Canva for drawing Matplotlib figures in a PyQt5
        window.
    """
    def __init__(self):
        """
            Init the PltWindow. Create the figure, the Canva and plot an empty
            graph inside the Canva using the figure. Add the toolbar from
            matplotlib on the top of it.
        """
        super().__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)


class PltWindowReading(PltWindow):
    
    def __init__(self):
        """
            Init the PltWindowProfile.
        """
        super().__init__()
        self.plot()

    def plot(self, data=None, name="", xlog = False, ylog = False, x_label="", y_label="", xlim="", xlimmax=""):
        """
            Plot the graph given the parameters.
            If data is None, plot an empty graph.
            If xlog is True, the x axis xill be logscale.
            The same goes for ylog.
            x_label and y_label designate the name of the axis.
            
            The folloxing arguements does not have any effect, but were let
            here to facilitate their implementation in case of need.
            xlim: position of a vertical line of equation x=xlim. Should be used to indicate the minimum limit of a graph. 
            xlimmax: position of a vertical line of equation x=xlimmax. Should be used to indicate the maximum limit of a graph. 
        """
        if data is None:
            data = []
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(data, "o--")
        else:
            ax = self.figure.add_subplot(111)
            if xlog:
                ax.set_xscale("log", nonposx='clip')
            if ylog:
                ax.set_yscale("log", nonposy='clip')
            x, y = data
            ax.plot(x, y, label=name)
            """
            if xlim:
                ax.axvline(x=xlim, linestyle="--", color="red", label="300 K")
            if xlimmax[0]:
                ax.axvline(x=xlimmax[0], linestyle="--", color="green", label=str(xlimmax[1]) + " K")
            """
            ax.legend()
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
        self.canvas.draw()

    def clear(self):
        self.figure.clear()


class PltWindowProfile(PltWindow):
    
    def __init__(self):
        """
            Init the PltWindowProfile.
        """
        super().__init__()
        self.plot()

    def plot(self, data=None, name="", xlog = False, ylog = False, x_label="", y_label="", xlim="", xlimmax=""):
        """
            Plot the graph given the parameters.
            If data is None, plot an empty graph.
            If xlog is True, the x axis xill be logscale.
            The same goes for ylog.
            x_label and y_label designate the name of the axis.
            
            The folloxing arguements does not have any effect, but were let
            here to facilitate their implementation in case of need.
            xlim: position of a vertical line of equation x=xlim. Should be used to indicate the minimum limit of a graph. 
            xlimmax: position of a vertical line of equation x=xlimmax. Should be used to indicate the maximum limit of a graph. 
        """
        if data is None:
            data = []
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(data, "o--")
        else:
            ax = self.figure.add_subplot(111)
            if xlog:
                ax.set_xscale("log", nonposx='clip')
            if ylog:
                ax.set_yscale("log", nonposy='clip')
            x, y = data
            ax.plot(x, y, label=name)
            """
            if xlim:
                ax.axvline(x=xlim, linestyle="--", color="red", label="300 K")
            if xlimmax[0]:
                ax.axvline(x=xlimmax[0], linestyle="--", color="green", label=str(xlimmax[1]) + " K")
            """
            ax.legend()
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
        self.canvas.draw()

    def clear(self):
        self.figure.clear()