# SkyPointer

## Introduction

A laser pointer controlled by software.

The following diagram shows the current setup:

```
 +------------+  TCP     +------------+            +------------+ 
 |            |  socket  | SkyPointer | USB-serial | SkyPointer | 
 | Stellarium +--------->| controller +----------->| hardware   | 
 |            |          |  (Python)  |            | (Arduino)  | 
 +------------+          +------------+            +------------+ 
```

## Hardware

An Arduino Uno board controls two stepper motors (azimuth and elevation) using an
[Adafruit Motor Shield V2](https://www.adafruit.com/products/1438).


## Software

The software controller is coded in Python.
This project implements a TCP server that receives messages from
[Stellarium](http://www.stellarium.org/) using its
[client-server protocol](http://www.stellarium.org/wiki/index.php/Telescope_Control_%28client-server%29).


## Installing

### Installing the Arduino firmware

* Download the code with `git clone https://github.com/juanmb/SkyPointer.git`
* Install the [TimerOne](https://github.com/PaulStoffregen/TimerOne) library
* Install the [ArduinoSerialCommand](https://github.com/scogswell/ArduinoSerialCommand)
  library
* Copy the `arduino/skypointer_motorshield` folder to your Arduino `libraries`
  directory (or make a symlink to it)
* Open the file `arduino/skypointer/skypointer.ino` in the Arduino IDE, compile
  it and upload it to your Arduino Uno board


### Installing the Python package in Debian/Ubuntu

Install required Python dependencies

```
$ sudo apt-get install pyqt4-dev-tools python-numpy
```

Now you can install the *skypointer* package with pip

```
$ pip install skypointer
```

Or downloading the source and calling `setup.py` directly from the `python` folder

```
$ git clone https://github.com/juanmb/SkyPointer.git
$ cd python
$ python setup.py install
```

For development, it is strongly recommended to install this package into a
[virtual environment](https://virtualenv.pypa.io/en/latest/).


### Installing the Python package in Windows

Using [Anaconda](https://www.continuum.io/downloads):

```
conda install numpy pyserial pyqt
```

Now you can install the skypointer package using pip

```
$ pip install skypointer
```

Or downloading the source and calling `setup.py` directly from the `python` folder

```
$ git clone https://github.com/juanmb/SkyPointer.git
$ cd python
$ python setup.py install
```

## Usage

Run `skypointer-gui`.


## Communication with Stellarium

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
