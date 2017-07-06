from PyQt4 import QtCore, QtGui

def gui_fname(dir=None, index=0):
    """Select a file via a dialog and returns the file name.
    """
    if dir is None: dir ='./'
    message = "Select Folder #%d" %index
    dir_name = QtGui.QFileDialog.getExistingDirectory(None, message,
                                                  dir,
                                                  QtGui.QFileDialog.ShowDirsOnly)
    return dir_name


def gui_output_folder(dir=None):
    """Select a folder
    """
    if dir is None: dir ='./'
    dir_name = QtGui.QFileDialog.getExistingDirectory(None, "Select Folder ...",
                                                  dir,
                                                  QtGui.QFileDialog.ShowDirsOnly)
    return dir_name
