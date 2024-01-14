from main import MainWindow
import sys
from PyQt6 import QtCore, QtWidgets
import platform

# op_sys = platform.system()
# if op_sys == 'Darwin':
#     from Foundation import NSURL

class DragAndDropWindow(QtWidgets.QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('PyShine drag drop plot')
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self,e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self,e):
        if e.mimeData().hasUrls():
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            for url in e.mimeData().urls():
                # if op_sys == 'Darwin':
                #     fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
                # else:
                fname = str(url.toLocalFile())
                self.filename = fname
                print("GOT ADDRESS:", self.filename)
                self.readData()
        else:
            e.ignore()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DragAndDropWindow()
    window.show()
    sys.exit(app.exec())