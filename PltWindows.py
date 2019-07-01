from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout
                            )
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.ticker as mtick
import numpy as np

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
    
    # def plot(self, data=None, name="", xlog = False, ylog = False, x_label="", y_label="", xlim="", xlimmax=""):
    def plot(self, data=None, name="", xlog = False, ylog = False, x_label="", y_label=""):
        """
            Plot the graph given the parameters.
            If data is None, plot an empty graph.
            If xlog is True, the x axis xill be logscale.
            The same goes for ylog.
            x_label and y_label designate the name of the axis.
        """
            # xlim: position of a vertical line of equation x=xlim. Should be used to indicate the minimum limit of a graph. 
            # xlimmax: position of a vertical line of equation x=xlimmax. Should be used to indicate the maximum limit of a graph. 

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
            # if xlim:
            #     ax.axvline(x=xlim, linestyle="--", color="red", label="300 K")
            # if xlimmax[0]:
            #     ax.axvline(x=xlimmax[0], linestyle="--", color="green", label=str(xlimmax[1]) + " K")
            ax.grid()
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
        self.xmin = None
        self.xmax = None
    
    def getXminFromVector(self, abscissa):
        return abscissa[0]

    def getXmaxFromVector(self, abscissa, ordinate):
        xmax_of_this_vect = None
        #todo: np.isnan
        dyx = np.abs(np.gradient(ordinate, abscissa))
        dyx_trigger = np.max(dyx) / 10
        for x, derivate in zip(abscissa[::-1], dyx[::-1]):
            if derivate <= dyx_trigger:
                xmax_of_this_vect = x
            else:
                break
        print(xmax_of_this_vect)
        return xmax_of_this_vect

    # def plot(self, data=None, name="", xlog = False, ylog = False, x_label="", y_label=""):
    def plot(self, data=None, name="", xlog = False, ylog = False, x_label="", y_label="", linestyle=""):
        """
            Plot the graph given the parameters.
            If data is None, plot an empty graph.
            If xlog is True, the x axis xill be logscale.
            The same goes for ylog.
            x_label and y_label designate the name of the axis.
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

            ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
            """
            xmaxtemp = self.getXmaxFromVector(x, y)
            if self.xmax:
                if self.xmax < xmaxtemp:
                    self.xmax = xmaxtemp
            elif xmaxtemp:
                self.xmax = xmaxtemp
            if self.xmax:
                ax.set_xlim(right=self.xmax)
            
            xmintemp = self.getXminFromVector(x)
            if self.xmin:
                if self.xmin > xmintemp:
                    self.xmin = xmintemp
            elif xmintemp:
                self.xmin = xmintemp
            if self.xmin:
                ax.set_xlim(left=self.xmin)
            #ax.set_xlim(left=0)
            #ax.set_xlim(right=1e-8)
            """
            if linestyle:
                ax.plot(x, y, linestyle, label=name)
            else:
                ax.plot(x, y, label=name)
            ax.legend()
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
        self.canvas.draw()

    def clear(self):
        self.xmax = None
        self.figure.clear()