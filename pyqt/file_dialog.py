from PyQt4 import QtCore, QtGui

class FileDialog(QtGui.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setOption(QtGui.QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QtGui.QFileDialog.ExistingFiles)

    def accept(self):
        super(FileDialog, self).accept(self)

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__(self)
        self.button = QtGui.QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.button)

    def handleButton(self):
        dialog = FileDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            print(dialog.selectedFiles())

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())