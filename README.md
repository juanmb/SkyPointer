# SkyPointer

Software for controlling a motorized sky-pointing laser.

**This project is in a very early stage!!!**

## How it works

The following diagram shows the intended setup:

```
                          THIS PROJECT                            
 +------------+  TCP     +------------+            +------------+ 
 |            |  socket  | SkyPointer | USB-serial | SkyPointer | 
 | Stellarium +--------->| server     +----------->| hardware   | 
 |            |          |            |            | (Arduino)  | 
 +------------+          +------------+            +------------+ 
```

This project implements a TCP server that receives messages from [Stellarium](http://www.stellarium.org/)
using its [client-server protocol](http://www.stellarium.org/wiki/index.php/Telescope_Control_%28client-server%29).

## Installation

Using pip:

```
$ pip install skypointer
```

Calling `setup.py` directly:

```
$ python setup.py install
```

Installation in *development mode* (recommended for developers):

```
$ python setup.py develop
```

For development, it is strongly recommended to install this package into a
[virtual environment](https://virtualenv.pypa.io/en/latest/).

## Configuration

* Call `sky-pointer` with the appropiate arguments from the command line
  (Use `-h` for getting help about the available options).

* Start Stellarium

* Enable the plugin *Telescope control* in Stellarium. If it was disabled,
  you will need to restart Stellarium (only the first time).

* In the configuration window of the *Telescope control* plugin, add a new
  telescope and select the option "External software or a remote computer".

* Choose a name and select "Equinox of the date (JNow)".

* Enter the TCP port 100001 (or the port you passed to the `sky-pointer` command).

* Close the dialog and press "Connect".

Now you can send the equatorial coordinates of the selected object in
Stellarium to the *SkyPointer* server by pressing `Ctrl+1`.

## Configuration file

sky-pointer reads a configuration file that can be located at the following
places:

* `~/.config/sky-pointer`

* `~/.sky-pointer/config`

* `~/sky-pointerrc`

* `/etc/sky-pointer/config`

This is an example of a valid configuration file:

```
[sky-pointer]

serial = /dev/ttyUSB0
joystick = /dev/input/js0
iface = 0.0.0.0
port = 10000

# mechanical errors (in radians)
z1 = 0.0
z2 = 0.0
z3 = 0.0
```

The options defined in the configuration file will be overriden by the
command-line arguments, except the mechanical errors.
