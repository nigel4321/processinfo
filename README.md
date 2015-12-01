# Process information (Linux)

A module to gather various peices of information about a process
(Useful for versions of python which do not support psutil)

There are no additional dependencies, all process information if gathered from /proc

Gather information on:
* CPU use (as a percentage)
* Number of open file descriptors
* Number of threads
* Number of sockets for tcp, tcp6, udp, udp6 and unix

