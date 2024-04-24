import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Plot Window")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget to hold the plot
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Create a figure and canvas
        self.figure, self.canvas = plt.subplots()
        self.canvas = FigureCanvas(self.figure)  # Corrected line
        layout.addWidget(self.canvas)

        # Your plotting code
        self.plot_data()

    def plot_data(self):
        # Plot some data
        x = [1, 2, 3, 4]
        y = [10, 5, 7, 3]
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(x, y)
        self.canvas.draw()

if __name__ == "__main__":
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create and show the plot window
    plot_window = PlotWindow()
    plot_window.show()
    input("wtf")

    # Start the Qt event loop
    sys.exit(app.exec_())
