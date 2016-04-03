# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'goto_dlg.ui'
#
# Created: Sat Apr  2 18:43:03 2016
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

class Ui_GotoDialog(object):
    def setupUi(self, GotoDialog):
        GotoDialog.setObjectName(_fromUtf8("GotoDialog"))
        GotoDialog.resize(272, 202)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GotoDialog.sizePolicy().hasHeightForWidth())
        GotoDialog.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtGui.QWidget(GotoDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 10, 251, 183))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.star_name_combo = QtGui.QComboBox(self.verticalLayoutWidget)
        self.star_name_combo.setObjectName(_fromUtf8("star_name_combo"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.star_name_combo)
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.star_bayer_combo = QtGui.QComboBox(self.verticalLayoutWidget)
        self.star_bayer_combo.setObjectName(_fromUtf8("star_bayer_combo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.star_bayer_combo)
        self.verticalLayout.addLayout(self.formLayout)
        self.line = QtGui.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.ra_m = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.ra_m.setMaximum(59)
        self.ra_m.setObjectName(_fromUtf8("ra_m"))
        self.gridLayout.addWidget(self.ra_m, 0, 2, 1, 1)
        self.ra_s = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.ra_s.setMaximum(59)
        self.ra_s.setObjectName(_fromUtf8("ra_s"))
        self.gridLayout.addWidget(self.ra_s, 0, 3, 1, 1)
        self.dec_m = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.dec_m.setMaximum(59)
        self.dec_m.setObjectName(_fromUtf8("dec_m"))
        self.gridLayout.addWidget(self.dec_m, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.dec_s = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.dec_s.setMaximum(59)
        self.dec_s.setObjectName(_fromUtf8("dec_s"))
        self.gridLayout.addWidget(self.dec_s, 1, 3, 1, 1)
        self.ra_h = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.ra_h.setMaximum(23)
        self.ra_h.setObjectName(_fromUtf8("ra_h"))
        self.gridLayout.addWidget(self.ra_h, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dec_d = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.dec_d.setMinimum(-90)
        self.dec_d.setMaximum(90)
        self.dec_d.setObjectName(_fromUtf8("dec_d"))
        self.gridLayout.addWidget(self.dec_d, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_2 = QtGui.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GotoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GotoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GotoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GotoDialog)

    def retranslateUi(self, GotoDialog):
        GotoDialog.setWindowTitle(_translate("GotoDialog", "Go to...", None))
        self.label_3.setText(_translate("GotoDialog", "By name:", None))
        self.label_4.setText(_translate("GotoDialog", "Bayer id:", None))
        self.label_2.setText(_translate("GotoDialog", "Dec:", None))
        self.label.setText(_translate("GotoDialog", "RA:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GotoDialog = QtGui.QDialog()
    ui = Ui_GotoDialog()
    ui.setupUi(GotoDialog)
    GotoDialog.show()
    sys.exit(app.exec_())

