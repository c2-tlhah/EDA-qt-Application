import os
import sys

from findPathWidget import FindPathWidget
from imageView import ImageView
from script import get_df, CHART_TYPE_DICT, TEMP_SAVE_FILENAME, summary

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QVBoxLayout, QWidget, QStackedWidget, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QSplitter, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, QCoreApplication, QThread
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        try:
            pass
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__df, self.__last_column = '', ''

    def __initUi(self):
        self.setWindowTitle('Chart Helper for Exploratory Data Analysis')
        findPathWidget = FindPathWidget()
        findPathWidget.getLineEdit().setPlaceholderText('Choose the CSV file...')
        findPathWidget.setExtOfFiles('CSV Files (*.csv)')
        findPathWidget.added.connect(self.__initGraph)
        self.__chartTypeCmbBox = QComboBox()
        self.__chartTypeCmbBox.addItems(list(CHART_TYPE_DICT.keys()))
        self.__chartTypeCmbBox.setCurrentIndex(1)

        self.__chartTypeCmbBox.currentTextChanged.connect(self.__drawGraph)
        self.__chartTypeCmbBox.setEnabled(False)

        self.__graphStackWidget = QStackedWidget()

        self.__view = ImageView()

        self.__dataFrameInformationTableWidget = QTableWidget()

        lay = QHBoxLayout()
        lay.addWidget(self.__dataFrameInformationTableWidget)
        lay.addWidget(self.__view)
        lay.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter()
        splitter.addWidget(self.__dataFrameInformationTableWidget)
        splitter.addWidget(self.__view)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([300, 700])
        splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")
        splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        lay = QVBoxLayout()
        lay.addWidget(findPathWidget)
        lay.addWidget(self.__chartTypeCmbBox)
        lay.addWidget(splitter)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def __initDataFrame(self, filename):
        self.__df, self.__last_column = get_df(filename)
        shape, summ = summary(self.__df)

        self.__dataFrameInformationTableWidget.clear()

        self.__dataFrameInformationTableWidget.setRowCount(summ.shape[0])
        self.__dataFrameInformationTableWidget.setColumnCount(summ.shape[1])
        self.__dataFrameInformationTableWidget.setHorizontalHeaderLabels(summ.columns.astype(str))
        self.__dataFrameInformationTableWidget.setVerticalHeaderLabels(self.__df.columns)

        for i in range(summ.shape[0]):
            for j in range(summ.shape[1]):
                item = QTableWidgetItem(str(summ.iloc[i, j]))
                item.setFlags(Qt.ItemIsEnabled)
                self.__dataFrameInformationTableWidget.setItem(i, j, item)

    def __drawGraph(self):
        f = CHART_TYPE_DICT[self.__chartTypeCmbBox.currentText()](self.__df, self.__last_column)
        if f:
            self.__loadGraph()
        else:
            QMessageBox.information(self, 'Sorry', 'There is nothing to show.')

    def __loadGraph(self):
        self.__view.setFilename(TEMP_SAVE_FILENAME)

    def __initGraph(self, filename):
        self.__initDataFrame(filename)
        self.__drawGraph()
        self.__chartTypeCmbBox.setEnabled(True)

    def closeEvent(self, e):
        super().closeEvent(e)
        if os.path.exists(TEMP_SAVE_FILENAME):
            os.remove(TEMP_SAVE_FILENAME)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())