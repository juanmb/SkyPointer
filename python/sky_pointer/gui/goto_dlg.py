# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'goto_dlg.ui'
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

class Ui_GotoDialog(object):
    def setupUi(self, GotoDialog):
        GotoDialog.setObjectName(_fromUtf8("GotoDialog"))
        GotoDialog.setEnabled(True)
        GotoDialog.resize(250, 201)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GotoDialog.sizePolicy().hasHeightForWidth())
        GotoDialog.setSizePolicy(sizePolicy)
        GotoDialog.setModal(True)
        self.gridLayout_2 = QtGui.QGridLayout(GotoDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.star_name_combo = QtGui.QComboBox(GotoDialog)
        self.star_name_combo.setObjectName(_fromUtf8("star_name_combo"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.star_name_combo)
        self.label_4 = QtGui.QLabel(GotoDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.star_bayer_combo = QtGui.QComboBox(GotoDialog)
        self.star_bayer_combo.setObjectName(_fromUtf8("star_bayer_combo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.star_bayer_combo)
        self.label_3 = QtGui.QLabel(GotoDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.verticalLayout.addLayout(self.formLayout)
        self.line = QtGui.QFrame(GotoDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.ra_m = QtGui.QSpinBox(GotoDialog)
        self.ra_m.setMaximum(59)
        self.ra_m.setObjectName(_fromUtf8("ra_m"))
        self.gridLayout.addWidget(self.ra_m, 0, 2, 1, 1)
        self.ra_s = QtGui.QSpinBox(GotoDialog)
        self.ra_s.setMaximum(59)
        self.ra_s.setObjectName(_fromUtf8("ra_s"))
        self.gridLayout.addWidget(self.ra_s, 0, 3, 1, 1)
        self.dec_m = QtGui.QSpinBox(GotoDialog)
        self.dec_m.setMaximum(59)
        self.dec_m.setObjectName(_fromUtf8("dec_m"))
        self.gridLayout.addWidget(self.dec_m, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(GotoDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.dec_s = QtGui.QSpinBox(GotoDialog)
        self.dec_s.setMaximum(59)
        self.dec_s.setObjectName(_fromUtf8("dec_s"))
        self.gridLayout.addWidget(self.dec_s, 1, 3, 1, 1)
        self.ra_h = QtGui.QSpinBox(GotoDialog)
        self.ra_h.setMaximum(23)
        self.ra_h.setObjectName(_fromUtf8("ra_h"))
        self.gridLayout.addWidget(self.ra_h, 0, 1, 1, 1)
        self.label = QtGui.QLabel(GotoDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dec_d = QtGui.QSpinBox(GotoDialog)
        self.dec_d.setMinimum(-90)
        self.dec_d.setMaximum(90)
        self.dec_d.setObjectName(_fromUtf8("dec_d"))
        self.gridLayout.addWidget(self.dec_d, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_2 = QtGui.QFrame(GotoDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.buttonBox = QtGui.QDialogButtonBox(GotoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(GotoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GotoDialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GotoDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(GotoDialog)
        GotoDialog.setTabOrder(self.star_name_combo, self.star_bayer_combo)
        GotoDialog.setTabOrder(self.star_bayer_combo, self.ra_h)
        GotoDialog.setTabOrder(self.ra_h, self.ra_m)
        GotoDialog.setTabOrder(self.ra_m, self.ra_s)
        GotoDialog.setTabOrder(self.ra_s, self.dec_d)
        GotoDialog.setTabOrder(self.dec_d, self.dec_m)
        GotoDialog.setTabOrder(self.dec_m, self.dec_s)
        GotoDialog.setTabOrder(self.dec_s, self.buttonBox)

    def retranslateUi(self, GotoDialog):
        GotoDialog.setWindowTitle(_translate("GotoDialog", "Go to...", None))
        self.label_4.setText(_translate("GotoDialog", "Bayer id:", None))
        self.label_3.setText(_translate("GotoDialog", "By name:", None))
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

