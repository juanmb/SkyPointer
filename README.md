# SkyPointer

## Description

An open-hardware altazimuth mount with a laser pointer.

The following block diagram shows the current setup:

![](images/blocks.png?raw=true "Block diagram")

## CAD

The SkyPointer mechanical parts were designed to be easily fabricated with a 3D
printer. The `cad` folder contains the CAD files in Step, STL and
[FreeCAD](http://www.freecadweb.org) formats.

## Electronics

Circuit schematics and PCB layout were designed with [Kicad](http://kicad-pcb.org).
They are stored in the `kicad` folder.

## Arduino

An Arduino Uno board controls two stepper motors (azimuth and elevation) using
a [CNC shield](http://blog.protoneer.co.nz/arduino-cnc-shield/) with some
modifications (documentation in progress).

The Arduino firmware is located in a
[separate repo](https://github.com/davidvg/ArduinoSkyPointer).

## The Python server

![](images/server_screenshot.png?raw=true "Screenshot of the server GUI")

The server receives "goto" messages from
[Stellarium](http://www.stellarium.org/) and sends "current position" packets back.

The Stellarium client-server protocol is documented
[here](http://www.stellarium.org/wiki/index.php/Telescope_Control_%28client-server%29).


### Installing the server in GNU/Linux

Install the required dependencies using your package manager. In Debian/Ubuntu,
you can use apt-get like this

```
$ sudo apt-get install pyqt4-dev-tools python-numpy python-scipy
```

Now you can install the *skypointer* package with pip

```
$ sudo pip install skypointer
```

Alternatively, you can clone this repo and call `setup.py` directly from the
`python` folder

```
$ git clone https://github.com/juanmb/SkyPointer.git
$ cd python
$ python setup.py install
```

For development, it is strongly recommended to install this package into a
[virtual environment](https://virtualenv.pypa.io/en/latest/).


### Installing the server in Windows

Using [Anaconda](https://www.continuum.io/downloads):

```
conda install numpy scipy pyserial pyqt
```

Now you can install the skypointer package using pip

```
$ pip install skypointer
```

### Usage

Run `skypointer-gui`.


### Communication with Stellarium

* Start `skypointer-gui`.

* Check *Enable server* in the *Configuration* tab, select a server port number
  and click *Apply*.

* Start Stellarium.

* Enable the plugin *Telescope control* in Stellarium. If it was disabled,
  you will need to restart Stellarium (only the first time).

* In the configuration window of the *Telescope control* plugin, add a new
  telescope and select the option "External software or a remote computer".

* Choose a name and select "Equinox of the date (JNow)".

* Enter the TCP port of the server.

* Close the dialog and press "Connect".

Now you can send the equatorial coordinates of the selected object in
Stellarium to the *SkyPointer* server by pressing `Ctrl+1`.
