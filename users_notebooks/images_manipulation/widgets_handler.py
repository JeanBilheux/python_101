try:
    from PyQt4 import QtCore, QtGui
    from PyQt4.QtGui import QFileDialog
except:
    from PyQt5 import QtGui, QtCore
    from PyQt5.qtwidgets import QFileDialog

def gui_fname(dir=None, index=0):
    """Select a file via a dialog and returns the file name.
    """
    if dir is None: dir ='./'
    message = "Select Folder #%d" %index
    dir_name = QFileDialog.getExistingDirectory(None, message,
                                                  dir,
                                                  QFileDialog.ShowDirsOnly)
    return dir_name


def gui_output_folder(dir=None):
    """Select a folder
    """
    if dir is None: dir ='./'
    dir_name = QFileDialog.getExistingDirectory(None, "Select Folder ...",
                                                  dir,
                                                  QFileDialog.ShowDirsOnly)
    return dir_name


class FileDialog(QFileDialog):
        def __init__(self, *args):
            QFileDialog.__init__(self, *args)
            self.setOption(self.DontUseNativeDialog, True)
            self.setFileMode(self.DirectoryOnly)

            self.tree = self.findChild(QtGui.QTreeView)
            self.tree.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

            self.list = self.findChild(QtGui.QListView)
            self.list.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

def gui_fnames(dir=None):
    """Select a list of folders"""
    if dir is None: dir ='./'
    message = "Select all the folders to add"
    dir_names = FileDialog()
    dir_names.show()