# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calib_dlg.ui'
#
# Created: Mon Apr  4 00:04:06 2016
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(194, 146)
        Dialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setHorizontalSpacing(12)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.z1Label = QtGui.QLabel(Dialog)
        self.z1Label.setObjectName(_fromUtf8("z1Label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.z1Label)
        self.z2Label = QtGui.QLabel(Dialog)
        self.z2Label.setObjectName(_fromUtf8("z2Label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.z2Label)
        self.z3Label = QtGui.QLabel(Dialog)
        self.z3Label.setObjectName(_fromUtf8("z3Label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.z3Label)
        self.z1Value = QtGui.QDoubleSpinBox(Dialog)
        self.z1Value.setDecimals(4)
        self.z1Value.setMinimum(-1.0)
        self.z1Value.setMaximum(1.0)
        self.z1Value.setSingleStep(0.01)
        self.z1Value.setObjectName(_fromUtf8("z1Value"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.z1Value)
        self.z2Value = QtGui.QDoubleSpinBox(Dialog)
        self.z2Value.setDecimals(4)
        self.z2Value.setMinimum(-1.0)
        self.z2Value.setMaximum(1.0)
        self.z2Value.setSingleStep(0.01)
        self.z2Value.setObjectName(_fromUtf8("z2Value"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.z2Value)
        self.z3Value = QtGui.QDoubleSpinBox(Dialog)
        self.z3Value.setDecimals(4)
        self.z3Value.setMinimum(-1.0)
        self.z3Value.setMaximum(1.0)
        self.z3Value.setSingleStep(0.01)
        self.z3Value.setObjectName(_fromUtf8("z3Value"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.z3Value)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.z1Value, self.z2Value)
        Dialog.setTabOrder(self.z2Value, self.z3Value)
        Dialog.setTabOrder(self.z3Value, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Calibration", None))
        self.z1Label.setText(_translate("Dialog", "Z1:", None))
        self.z2Label.setText(_translate("Dialog", "Z2:", None))
        self.z3Label.setText(_translate("Dialog", "Z3:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

