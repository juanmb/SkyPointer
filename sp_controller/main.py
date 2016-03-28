import sys
from functools import partial
import glob
import serial
from threading import Timer
from PyQt4 import QtCore, QtGui
from serial import SerialException
from sky_pointer.pointer import Pointer
from sky_pointer.coords import EqCoords
from math import pi
import main_dlg
import calib_dlg
import goto_dlg


def list_serial_ports():
    """Lists serial port names"""
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class CalibDialog(QtGui.QDialog, calib_dlg.Ui_Dialog):
    def __init__(self, parent=None, calib=(0, 0, 0)):
        super(CalibDialog, self).__init__(parent)
        self.setupUi(self)
        self.z1Value.setValue(calib[0])
        self.z2Value.setValue(calib[1])
        self.z3Value.setValue(calib[2])

    def getCalib(self):
        return self.z1Value.value(), self.z2Value.value(), \
            self.z3Value.value()

class GotoDialog(QtGui.QDialog, goto_dlg.Ui_GotoDialog):
    def __init__(self, parent=None):
        super(GotoDialog, self).__init__(parent)
        self.setupUi(self)

    def getTarget(self):
        ra_tgt = self.ra_h.value() + self.ra_min.value()/60. \
            + self.ra_sec.value()/3600.
        dec_tgt = self.dec_deg.value() + self.dec_min.value()/60. \
            + self.dec_sec.value()/3600.
        return EqCoords(ra_tgt*pi/12, dec_tgt*pi/180)


class MyApp(QtGui.QDialog, main_dlg.Ui_spcontroller):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)
        self.cfg = QtCore.QSettings('skypointer')
        self.run_tmr = Timer(0, None)

        # allow using the arrows keys
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

        # bind signals
        self.applyButton.clicked.connect(self.onApply)
        self.laserButton.clicked.connect(self.onLaser)
        self.upButton.pressed.connect(partial(self.onArrow, 'up', True))
        self.upButton.released.connect(partial(self.onArrow, 'up', False))
        self.downButton.pressed.connect(partial(self.onArrow, 'down', True))
        self.downButton.released.connect(partial(self.onArrow, 'down', False))
        self.leftButton.pressed.connect(partial(self.onArrow, 'left', True))
        self.leftButton.released.connect(partial(self.onArrow, 'left', False))
        self.rightButton.pressed.connect(partial(self.onArrow, 'right', True))
        self.rightButton.released.connect(partial(self.onArrow, 'right', False))
        self.gotoButton.clicked.connect(self.onGoto)
        self.alignButton.clicked.connect(self.onAlign)
        self.calibrateButton.clicked.connect(self.onCalibrate)

        for port in list_serial_ports():
            self.serialCombo.addItem(port)

        # load settings
        idx = self.serialCombo.findText(self.cfg.value('serial_port', type=str))
        self.serialCombo.setCurrentIndex(idx)
        idx = self.joystickCombo.findText(self.cfg.value('joystick', type=str))
        self.joystickCombo.setCurrentIndex(idx)
        self.enableServer.setChecked(self.cfg.value('enable_server', type=bool))
        self.localHostOnly.setChecked(self.cfg.value('localhost_only', type=bool))
        self.serverPort.setValue(self.cfg.value('server_port', type=int))

        self.connect_pointer()

    def setChildrenFocusPolicy (self, policy):
        def set_policy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtGui.QWidget):
                childQWidget.setFocusPolicy(policy)
                set_policy(childQWidget)
        set_policy(self)

    def connect_pointer(self):
        try:
            self.ptr = Pointer(str(self.cfg.value('serial_port', type=str)))
        except (SerialException, IOError) as e:
            self.statusDevice.setText('None')
            QtGui.QMessageBox.warning(self, "Serial error", str(e))
            self.ptr = None
        else:
            self.statusDevice.setText(self.ptr.get_id())
            self.update_calib()

        self.statusAligned.setText('No')
        self.coordBox.setEnabled(self.ptr is not None)
        self.controlBox.setEnabled(self.ptr is not None)

    def update_target(self):
        if self.ptr:
            tgt = self.ptr.target
            self.coordTarget.setText(str(tgt))
            self.alignButton.setEnabled(True)

    def update_calib(self):
        if self.ptr:
            calib = self.ptr.calib
            self.statusCalibration.setText(' '.join([("%.4f" % c) for c in calib]))

    def processKeyEvent(self, event, pressed):
        if event.isAutoRepeat():
            return
        key = event.key()
        if key == QtCore.Qt.Key_Right:
            self.rightButton.setDown(pressed)
            self.onArrow('right', pressed)
        elif key == QtCore.Qt.Key_Left:
            self.leftButton.setDown(pressed)
            self.onArrow('left', pressed)
        elif key == QtCore.Qt.Key_Up:
            self.upButton.setDown(pressed)
            self.onArrow('up', pressed)
        elif key == QtCore.Qt.Key_Down:
            self.downButton.setDown(pressed)
            self.onArrow('down', pressed)

    def keyPressEvent(self, event):
        self.processKeyEvent(event, True)

    def keyReleaseEvent(self, event):
        self.processKeyEvent(event, False)

    def onApply(self):
        """Save settings"""
        self.cfg.setValue('serial_port', self.serialCombo.currentText())
        self.cfg.setValue('joystick', self.joystickCombo.currentText())
        self.cfg.setValue('enable_server', bool(self.enableServer.checkState()))
        self.cfg.setValue('localhost_only', bool(self.localHostOnly.checkState()))
        self.cfg.setValue('server_port', self.serverPort.value())
        print "Settings saved in", self.cfg.fileName()

        self.connect_pointer()

    def onLaser(self):
        if self.ptr:
            self.ptr.enable_laser(self.laserButton.isChecked())

    def onArrow(self, key, pressed):
        if pressed:
            az, el = 0, 0
            if key == 'right':
                az = 1
            elif key == 'left':
                az = -1
            elif key == 'up':
                el = 1
            elif key == 'down':
                el = -1

            self.ptr.steps(az, el)
            self.run_tmr.cancel()
            self.run_tmr = Timer(.5, self.ptr.run, (az, el))
            self.run_tmr.start()
        else:
            self.run_tmr.cancel()
            self.ptr.stop()

    def onCalibrate(self):
        dlg = CalibDialog(self, calib=self.ptr.calib)
        if dlg.exec_():
            self.ptr.set_calib(dlg.getCalib())
            self.update_calib()

    def onGoto(self):
        dlg = GotoDialog(self)
        if dlg.exec_():
            try:
                self.ptr.goto(dlg.getTarget())
            except ValueError:
                print "Not aligned"
            self.update_target()

    def onAlign(self):
        try:
            self.ptr.set_ref()
        except ValueError as e:
            QtGui.QMessageBox.warning(self, "Alignment error", str(e))

        npoints = self.ptr.get_nrefs()
        if npoints == 0:
            text = 'No'
        if npoints == 1:
            text = 'No (1 point)'
        else:
            text = 'Yes'

        self.statusAligned.setText(text)


def main():
    app = QtGui.QApplication(sys.argv)
    dlg = MyApp()
    dlg.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
