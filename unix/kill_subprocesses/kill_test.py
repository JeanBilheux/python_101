#!/usr/bin/env python
import sys, os, time,  psutil
import subprocess
from PyQt4 import QtGui, QtCore

import killGUI as gui


class App( QtGui.QMainWindow, gui.Ui_MainWindow):
    def __init__(self,parent=None):
        super(App, self).__init__(parent)
        self.parentProcess = psutil.Process(os.getpid())
        self.setupUi(self)

        self.statusBar.showMessage('Hello!')
        self.runButton.clicked.connect( self.launch )
        self.killButton.clicked.connect( self.slaughter)

    def launch(self):
        self.statusBar.showMessage('Running...')
        self.setStatusBar(self.statusBar)

        QtGui.QApplication.processEvents() 

        subprocess.Popen(['echo']) 
        subprocess.Popen(['sleep','5']) 
        self.runCheck()

    def runCheck( self ):
        print "--------------------------------------------"
        print "Parent process:", self.parentProcess.pid
        for kid in self.parentProcess.children():
            print "     ", "child process:", kid, "is running?",kid.status()!=psutil.STATUS_ZOMBIE
        print "--------------------------------------------"
        return
 
    def slaughter(self):
        for child in self.parentProcess.children(recursive=True):
            child.kill()
            child.wait()
        self.statusBar.showMessage('Killed')
        self.runCheck()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()
