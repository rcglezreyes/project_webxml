from PyQt5 import QtWidgets, QtCore

def center_window(view):
    frame = view.frameGeometry()
    center = QtWidgets.QDesktopWidget().availableGeometry().center()
    frame.moveCenter(center)
    view.move(frame.topLeft())
