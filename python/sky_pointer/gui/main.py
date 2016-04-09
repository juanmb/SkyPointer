import sys
import glob
import serial
from time import time
from functools import partial
from threading import Timer
from PyQt4 import QtCore, QtGui
from serial import SerialException
from sky_pointer.pointer import Pointer
from sky_pointer.coords import Coords, EqCoords
from sky_pointer.server import StellariumServerThread
from bright_stars import bright_stars
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
    def __init__(self, parent=None, target=EqCoords(0,0)):
        super(GotoDialog, self).__init__(parent)
        self.setupUi(self)

        by_bayer = sorted(bright_stars, key=lambda l: l[0])
        stars_by_bayer = [''] + [star[0] for star in by_bayer if star[0]]
        self.star_bayer_combo.addItems(stars_by_bayer)

        by_name = sorted(bright_stars, key=lambda l: l[1])
        stars_by_name = [''] + [star[1] for star in by_name if star[1]]
        self.star_name_combo.addItems(stars_by_name)

        self.fillCoords(target)

        self.star_bayer_combo.activated.connect(self.onSelectBayer)
        self.star_name_combo.activated.connect(self.onSelectName)

    def fillCoords(self, coords):
        # fill the values of the coordinate fields
        controls = self.ra_h, self.ra_m, self.ra_s, self.dec_d, self.dec_m, self.dec_s
        for control, v in zip(controls, coords.fields()):
            control.setValue(v)

    def onSelectBayer(self):
        self.star_name_combo.setCurrentIndex(0)
        name = self.star_bayer_combo.currentText()
        star = [star for star in bright_stars if star[0] == name][0]
        self.fillCoords(EqCoords(star[2], star[3]))

    def onSelectName(self):
        self.star_bayer_combo.setCurrentIndex(0)
        name = self.star_name_combo.currentText()
        star = [star for star in bright_stars if star[1] == name][0]
        self.fillCoords(EqCoords(star[2], star[3]))

    def getTarget(self):
        return EqCoords.from_fields(self.ra_h.value(), self.ra_m.value(),
                                    self.ra_s.value(), self.dec_d.value(),
                                    self.dec_m.value(), self.dec_s.value())


def requires_pointer(f):
    """Method decorator for checking that self.ptr is not None.
    If self.ptr is None, the function will return inmediately"""
    def wrapper(*args, **kwargs):
        if args[0].ptr is None:
            return
        return f(*args, **kwargs)
    return wrapper


class MyApp(QtGui.QDialog, main_dlg.Ui_spcontroller):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)
        self.cfg = QtCore.QSettings('skypointer')
        self.run_tmr = Timer(0, None)
        self.server = None
        self.ptr = None

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
        self.newPointButton.clicked.connect(self.onNewPoint)
        self.saveButton.clicked.connect(self.onSavePoints)
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
        self.start_server()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_coords)
        self.timer.start(1000)

    def setChildrenFocusPolicy (self, policy):
        def set_policy (parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtGui.QWidget):
                childQWidget.setFocusPolicy(policy)
                set_policy(childQWidget)
        set_policy(self)

    def connect_pointer(self):
        if self.ptr:
            self.ptr.close()

        self.statusAligned.setText('No')

        try:
            self.ptr = Pointer(str(self.cfg.value('serial_port', type=str)))
        except (SerialException, IOError) as e:
            self.statusDevice.setText('None')
            QtGui.QMessageBox.warning(self, "Serial error", str(e))
            self.ptr = None
        else:
            self.statusDevice.setText(self.ptr.get_id())
            self.update_calib()
            #self.load_alignment()

        self.calibrateButton.setEnabled(True)
        self.coordBox.setEnabled(self.ptr is not None)
        self.controlBox.setEnabled(self.ptr is not None)

    @requires_pointer
    def load_alignment(self):
        """load last stored alignment. It doesn't work, because the motors do
        not maintain its position after shut down.
        """

        def load(key):
            val, ok = self.cfg.value(key).toDouble()
            if not ok:
                raise ValueError
            return val

        try:
            eq1 = EqCoords(load('ref1_ra'), load('ref1_dec'))
            ins1 = Coords(load('ref1_az'), load('ref1_el'))
            print eq1, ins1
            self.ptr.set_ref(eq1, ins1, load('ref1_t'))

            eq2 = EqCoords(load('ref2_ra'), load('ref2_dec'))
            ins2 = Coords(load('ref2_az'), load('ref2_el'))
            print eq2, ins2
            self.ptr.set_ref(eq2, ins2, load('ref2_t'))

            print "Restored last alignment"
            self.statusAligned.setText('Yes (last)')
        except ValueError as e:
            print e


    def start_server(self):
        enable = self.cfg.value('enable_server', type=bool)
        host = '127.0.0.1' if self.cfg.value('localhost_only') else '0.0.0.0'
        port = self.cfg.value('server_port', type=int)
        print enable, host, port

        if enable and not self.server:
            print "Running server on %s:%d" % (host, port)
            self.server = StellariumServerThread(host, port, goto=self.set_target)
            self.server.start()

    @requires_pointer
    def set_target(self, target):
        self.coordTarget.setText(str(target))
        self.alignButton.setEnabled(True)

        try:
            self.ptr.goto(target)
        except ValueError:
            print "Not aligned"

    @requires_pointer
    def update_coords(self):
        if len(self.ptr.get_refs()) == 2:
            pos = self.ptr.get_coords()
            self.coordCurrent.setText(str(pos))
            if self.server:
                self.server.set_pos(pos)

    @requires_pointer
    def update_calib(self):
        calib = self.ptr.calib
        self.statusCalibration.setText(' '.join([("%.4f" % c) for c in calib]))

    @requires_pointer
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

    def onApply(self, _):
        """Save settings"""
        self.cfg.setValue('serial_port', self.serialCombo.currentText())
        self.cfg.setValue('joystick', self.joystickCombo.currentText())
        self.cfg.setValue('enable_server', bool(self.enableServer.checkState()))
        self.cfg.setValue('localhost_only', bool(self.localHostOnly.checkState()))
        self.cfg.setValue('server_port', self.serverPort.value())

        text = "The server settings will be applied\nwhen you restart the program.\n\n" \
            "Configuration saved in\n%s" % self.cfg.fileName()
        QtGui.QMessageBox.information(self, "Applied", text)

        self.connect_pointer()
        self.start_server()

    @requires_pointer
    def onLaser(self, checked):
        self.ptr.enable_laser(checked)

    @requires_pointer
    def onArrow(self, key, pressed):
        if pressed:
            az, el = 0, 0
            if key == 'left':
                az = 1
            elif key == 'right':
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

    @requires_pointer
    def onCalibrate(self, _):
        dlg = CalibDialog(self, calib=self.ptr.calib)
        if dlg.exec_():
            self.ptr.set_calib(dlg.getCalib())
            self.update_calib()
            QtGui.QMessageBox.information(self, "Calibrated",
                                          "Calibration has been uploaded to the device")
            self.connect_pointer()

    def onSavePoints(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file')
        open(fname, 'w').write(self.textPoints.toPlainText())

    @requires_pointer
    def onGoto(self, _):
        dlg = GotoDialog(self, self.ptr.target)
        if dlg.exec_():
            self.set_target(dlg.getTarget())

    @requires_pointer
    def onAlign(self, _):
        try:
            self.ptr.set_ref()
        except ValueError as e:
            QtGui.QMessageBox.warning(self, "Alignment error", str(e))

        npoints = len(self.ptr.get_refs())
        if npoints == 0:
            text = 'No'
        if npoints == 1:
            text = 'No (1 point)'
        else:
            text = 'Yes (2 points)'
            self.newPointButton.setEnabled(True)

            # store the alignment references in the settings file
            #for i, ref in enumerate(self.ptr.get_refs()):
                #self.cfg.setValue('ref%d_ra' % (i+1), ref['eq'][0])
                #self.cfg.setValue('ref%d_dec' % (i+1), ref['eq'][1])
                #self.cfg.setValue('ref%d_az' % (i+1), ref['inst'][0])
                #self.cfg.setValue('ref%d_el' % (i+1), ref['inst'][1])
                #self.cfg.setValue('ref%d_t' % (i+1), ref['t'])

        self.statusAligned.setText(text)

    @requires_pointer
    def onNewPoint(self, _):
        tgt = self.ptr.target
        inst = self.ptr.get_inst_coords()
        line = "%.2f %.4f %.4f %.4f %.4f" % \
            (time(), tgt[0], tgt[1], inst[0], inst[1])
        self.textPoints.append(line)

    @requires_pointer
    def closeEvent(self, event):
        self.ptr.close()


def main():
    app = QtGui.QApplication(sys.argv)
    dlg = MyApp()
    dlg.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
