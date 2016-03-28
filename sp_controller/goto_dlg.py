# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'goto_dlg.ui'
#
# Created: Sat Mar 26 17:12:37 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GotoDialog(object):
    def setupUi(self, GotoDialog):
        GotoDialog.setObjectName(_fromUtf8("GotoDialog"))
        GotoDialog.resize(265, 134)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GotoDialog.sizePolicy().hasHeightForWidth())
        GotoDialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtGui.QDialogButtonBox(GotoDialog)
        self.buttonBox.setGeometry(QtCore.QRect(60, 100, 200, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(GotoDialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 31, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(GotoDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 31, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.ra_h = QtGui.QSpinBox(GotoDialog)
        self.ra_h.setGeometry(QtCore.QRect(60, 20, 60, 27))
        self.ra_h.setMaximum(23)
        self.ra_h.setObjectName(_fromUtf8("ra_h"))
        self.ra_min = QtGui.QSpinBox(GotoDialog)
        self.ra_min.setGeometry(QtCore.QRect(130, 20, 60, 27))
        self.ra_min.setMaximum(59)
        self.ra_min.setObjectName(_fromUtf8("ra_min"))
        self.ra_sec = QtGui.QSpinBox(GotoDialog)
        self.ra_sec.setGeometry(QtCore.QRect(200, 20, 60, 27))
        self.ra_sec.setMaximum(59)
        self.ra_sec.setObjectName(_fromUtf8("ra_sec"))
        self.dec_deg = QtGui.QSpinBox(GotoDialog)
        self.dec_deg.setGeometry(QtCore.QRect(60, 60, 60, 27))
        self.dec_deg.setMinimum(-90)
        self.dec_deg.setMaximum(90)
        self.dec_deg.setObjectName(_fromUtf8("dec_deg"))
        self.dec_min = QtGui.QSpinBox(GotoDialog)
        self.dec_min.setGeometry(QtCore.QRect(130, 60, 60, 27))
        self.dec_min.setObjectName(_fromUtf8("dec_min"))
        self.dec_sec = QtGui.QSpinBox(GotoDialog)
        self.dec_sec.setGeometry(QtCore.QRect(200, 60, 60, 27))
        self.dec_sec.setObjectName(_fromUtf8("dec_sec"))

        self.retranslateUi(GotoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GotoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GotoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GotoDialog)

    def retranslateUi(self, GotoDialog):
        GotoDialog.setWindowTitle(_translate("GotoDialog", "Dialog", None))
        self.label.setText(_translate("GotoDialog", "RA:", None))
        self.label_2.setText(_translate("GotoDialog", "Dec:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GotoDialog = QtGui.QDialog()
    ui = Ui_GotoDialog()
    ui.setupUi(GotoDialog)
    GotoDialog.show()
    sys.exit(app.exec_())

