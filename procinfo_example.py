import procinfo

procinfo = procinfo.ProcessInfo(2344)

print procinfo.socketcount()
print "Threads %s\n" % procinfo.threadcount()
print "File descriptors %s\n" % procinfo.fdcount()
print "Percent CPU %0.1f\n" % procinfo.cpuuse()
