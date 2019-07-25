from PyQt5.QtWidgets import (QWidget,
                             QVBoxLayout
                             )
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg \
    import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import FuncFormatter, FormatStrFormatter
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

        self.plotted_data = []

    def save(self, filename):
        """
            Save the Canva into txt, in the file 'filename'.
        """
        print(self.plotted_data)
        # list_x, list_y = [], []
        # for plot in plotted_data:
        #     x, y = plot
        #     list_x.append(x)
        #     list_y.append(y)

        # here, I want to be able to write the plot into a file. But what if a
        # plot has more points than the others? I want to plot the data like
        # this :
        # xa0, ya0; xb0, xb0
        # xa1, yx1; xb1, yb1
        # If xb and yb are too long, they will be printed after
        # the end of xa and ya, and the two column will combine.
        # That is why I need to save the longer set of data first.
        my_sort_function = lambda element: len(element[0])
        self.plotted_data.sort(key=my_sort_function)
        with open(filename, "w") as fichier:
            a_line_was_printed = True
            i = 0
            while a_line_was_printed:  # line
                # print("\n")
                if i % 100 == 0:
                    print("progression:", i, "/", len(self.plotted_data[0][0]))
                # print("let us start a new line")
                ligne = ""
                a_line_was_printed = False
                for plot in self.plotted_data:  # column
                    # print("in this line, i will write a plot:")
                    x, y = plot
                    # print("x=", x)
                    # print("y=", y)

                    if len(x) > i and len(y) > i:  # a data can be save
                        # print("The line ", i, "can be saved as ", x[i], y[i])
                        ligne += "{:.5e}".format(x[i]) + ", " + \
                            "{:.5e}".format(y[i]) + ";   "
                        a_line_was_printed = True
                # remove te last ";"
                ligne = ligne.rstrip(" ")
                ligne = ligne.rstrip(";")
                # print(ligne)
                fichier.write(ligne + "\n")
                i += 1


class PltWindowReading(PltWindow):

    def __init__(self):
        """
            Init the PltWindowProfile.
        """
        super().__init__()
        self.plot()

    # def plot(self, data=None, name="", xlog = False, ylog = False, \
    # x_label="", y_label="", xlim="", xlimmax=""):
    def plot(self, data=None, name="", xlog=False,
             ylog=False, x_label="", y_label=""):
        """
            Plot the graph given the parameters.
            If data is None, plot an empty graph.
            If xlog is True, the x axis xill be logscale.
            The same goes for ylog.
            x_label and y_label designate the name of the axis.
        """
        # xlim: position of a vertical line of equation x=xlim. Should
        # be used to indicate the minimum limit of a graph.
        # xlimmax: position of a vertical line of equation x=xlimmax. Should
        # be used to indicate the maximum limit of a graph.

        if data is None:
            data = []
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(data, "o--")
        else:
            ax = self.figure.add_subplot(111)
            ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            if xlog:
                ax.set_xscale("log", nonposx='clip')
            if ylog:
                ax.set_yscale("log", nonposy='clip')
            x, y = data
            ax.plot(x, y, label=name)
            # if xlim:
            #     ax.axvline(x=xlim, linestyle="--",
            #                color="red", label="300 K")
            # if xlimmax[0]:
            #     ax.axvline(x=xlimmax[0], linestyle="--",
            #                color="green", label=str(xlimmax[1]) + " K")
            # ax.grid()
            ax.legend()
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            self.plotted_data.append(data)
        # we don't need the previous grid, let's erase it
        ax.grid(False)
        ax.grid(True)
        self.canvas.draw()

    def clear(self):
        self.figure.clear()
        self.plotted_data = []


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
        # todo: np.isnan
        dyx = np.abs(np.gradient(ordinate, abscissa))
        dyx_trigger = np.max(dyx) / 10
        for x, derivate in zip(abscissa[::-1], dyx[::-1]):
            if derivate <= dyx_trigger:
                xmax_of_this_vect = x
            else:
                break
        print(xmax_of_this_vect)
        return xmax_of_this_vect

    def findXMinXMax(self, x, y):
        index_x_min = 0
        print("trouvons le x minimal")
        while y[index_x_min] < 1e-9:
            print(y[index_x_min])
            index_x_min += 1
            if index_x_min == len(x):
                # nothing interesting to plot here,
                # let's try to plot all the curve
                index_x_min = None
        print("fin", y[index_x_min])

        print("trouvons le x maximal")
        index_x_max = len(x) - 1
        while y[index_x_max] < 1e-9:
            print(y[index_x_max])
            index_x_max -= 1
            if index_x_max == 0:
                # nothing interesting to plot here,
                # let's try to plot all the curve
                index_x_max = None

        xmin = None if index_x_min is None else x[index_x_min]
        xmax = None if index_x_max is None else x[index_x_max]
        return xmin, xmax

    def updateXMinXMax(self, x, y):
        print("avant", self.xmin, self.xmax)
        xmin, xmax = self.findXMinXMax(x, y)

        if self.xmin and xmin:
            self.xmax = min(self.xmin, xmin)
        else:
            self.xmin = xmin

        if self.xmax and xmax:
            self.xmax = max(self.xmax, xmax)
        else:
            self.xmax = xmax
        print("apres", self.xmin, self.xmax)

    # def plot(self, data=None, name="", xlog = False,
    #          ylog = False, x_label="", y_label=""):
    def plot(self, data=None, name="", xlog=False,
             ylog=False, x_label="", y_label="", linestyle=""):
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

            majorFormatter = FuncFormatter(self.MyFormatter)
            ax.xaxis.set_major_formatter(majorFormatter)
            ax.yaxis.set_major_formatter(majorFormatter)
            self.updateXMinXMax(x, y)

            # xmaxtemp = self.getXmaxFromVector(x, y)
            # if self.xmax:
            #     if self.xmax < xmaxtemp:
            #         self.xmax = xmaxtemp
            # elif xmaxtemp:
            #     self.xmax = xmaxtemp
            # if self.xmax:
            #     ax.set_xlim(right=self.xmax)

            # xmintemp = self.getXminFromVector(x)
            # if self.xmin:
            #     if self.xmin > xmintemp:
            #         self.xmin = xmintemp
            # elif xmintemp:
            #     self.xmin = xmintemp
            # if self.xmin:
            #     ax.set_xlim(left=self.xmin)
            # ax.set_xlim(left=0)
            # ax.set_xlim(right=1e-8)

            # x, y = x[index_x_min:index_x_max], y[index_x_min:index_x_max]
            # ax.set_ylim([x[index_x_min], x[index_x_max]])
            ax.set_ylim([1e-9, 1e-1])
            ax.set_xlim(left=self.xmin)
            ax.set_xlim(right=self.xmax)
            if linestyle:
                ax.plot(x, y, linestyle, label=name)
            else:
                ax.plot(x, y, label=name)
            ax.legend()
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            self.plotted_data.append(data)

        self.canvas.draw()

    def clear(self):
        self.xmax = None
        self.xmin = None
        self.figure.clear()
        self.plotted_data = []
