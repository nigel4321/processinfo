#!/usr/bin/env python

import os
import re
import time


class ProcessInfo(object):
    """
    Get process information for Linux hosts from /proc
    No other dependencies are required.
    """
    class _ConnTable(object):
        def __init__(self):
            self.tcpinodes = dict()
            self.tcp6inodes = dict()
            self.udpinodes = dict()
            self.udp6inodes = dict()
            self.unixinodes = dict()

    def __init__(self, pid=None, window=0.3):
        self.CLOCKTICK = os.sysconf('SC_CLK_TCK')
        self.window = window
        if not pid:
            self.pid = str(os.getpid())
        else:
            self.pid = str(pid)
        self.allconns = self._ConnTable()

    def _gettime(self):
        try:
            cf = open("/proc/" + self.pid + "/stat", "r")
        except Exception as err:
            print("Failed: %s\n" % str(err))
            raise
        data = cf.readline()
        cf.close()
        data = data.split()
        # print data[13]
        ttime = int(data[13]) + int(data[14]) + int(data[15]) + int(data[16])
        stime = time.time()
        return (ttime, stime)

    def cpuuse(self):
        """
        Return CPU usage as a percentage
        """
        (t1, s1) = self._gettime()
        time.sleep(0.5)
        (t2, s2) = self._gettime()
        t = (t2 - t1) / float(self.CLOCKTICK)
        s = (s2 - s1)
        # print t2, " ", t1
        # print t, " ", s
        val = (t / s) * 100
        return val

    def fdcount(self):
        """
        Returns a count of the number of open file descriptors
        """
        count = len(os.listdir("/proc/%s/fd" % self.pid))
        return count

    def threadcount(self):
        """
        Returns the number of threads for the specifid PID
        """
        procstat = "/proc/%s/stat" % self.pid
        with open(procstat, 'r') as f:
            sline = f.readline()
        sline = sline.split()
        return int(sline[19])

    def _getallconns(self):
        try:
            tcpf = open("/proc/net/tcp", "r")
            udpf = open("/proc/net/udp", "r")
            unixf = open("/proc/net/unix", "r")
        except Exception, err:
            print("getconns %s\n" % str(err))
            raise
        ip6 = True
        try:
            tcp6f = open("/proc/net/tcp6", "r")
            udp6f = open("/proc/net/udp6", "r")
        except Exception, err:
            print("Error getting ipv6 info %s\n" % str(err))
            ip6 = False
        allconns = self._ConnTable()
        for onel in tcpf:
            onel = onel.split()
            allconns.tcpinodes[onel[9]] = None
        for onel in udpf:
            onel = onel.split()
            allconns.udpinodes[onel[9]] = None
        for onel in unixf:
            onel = onel.split()
            self.allconns.unixinodes[onel[6]] = None
        if ip6:
            for onel in tcp6f:
                onel = onel.split()
                allconns.tcp6inodes[onel[9]] = None
            for onel in udp6f:
                onel = onel.split()
                allconns.udp6inodes[onel[9]] = None
        return allconns

    def socketcount(self):
        """
        Returns a hash keyed by tcp, tcp6, usd, udp6 and unix
        The hash contains the number of sockets for each item
        """
        sockstat = dict()
        for i in ['tcp', 'tcp6', 'udp', 'udp6', 'unix']:
            sockstat[i] = 0
        try:
            fds = os.listdir("/proc/%s/fd" % self.pid)
        except Exception as err:
            print("Error reading  %s\n" % str(err))
            raise
        sck = []
        allconns = self._getallconns()
        for f in fds:
            try:
                s = os.readlink("/proc/%s/fd/%s" % (self.pid, f))
            except Exception, err:
                print("getsocktype %s" % str(err))
                continue
            if re.match('socket', s):
                sck.append(re.search('[0-9]+', s).group(0))
        for i in sck:
            if i in allconns.tcpinodes:
                sockstat['tcp'] += 1
            elif i in allconns.tcpinodes:
                sockstat['tcp6'] += 1
            elif i in allconns.udpinodes:
                sockstat['udp'] += 1
            elif i in allconns.udp6inodes:
                sockstat['udp6'] += 1
            elif i in allconns.unixinodes:
                sockstat['unix'] += 1
        return sockstat

if __name__ == "__main__":
    help(__name__)
