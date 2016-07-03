# Process information (Linux)

A module to gather various peices of information about a process
(Useful for versions of python which do not support psutil)

There are no additional dependencies, all process information if gathered from /proc

Gather information on:
* CPU use (as a percentage)
* Number of open file descriptors
* Number of threads
* Number of sockets for tcp, tcp6, udp, udp6 and unix
* IO information, bytes read, written
* Memory usage information

### Example
```
$ python procinfo_example.py
Network connections {'udp6': 0, 'udp': 1, 'unix': 0, 'tcp6': 0, 'tcp': 10}

Threads 52

File descriptors 139

Percent CPU 3.0

IO information {'write_bytes': 59744256, 'read_bytes': 1384448, 'cancelled_write_bytes': 5296128, 'syscr': 169235, 'wchar': 52513446, 'rchar': 187726452, 'syscw': 86790}

Memory usage {'resident': 130117632, 'shared': 7491584, 'total': 1302380544}
```
