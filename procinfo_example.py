import procinfo

procinfo = procinfo.ProcessInfo(1104)

print "Network connections %s\n" % procinfo.netstats()
print "Threads %s\n" % procinfo.threadcount()
print "File descriptors %s\n" % procinfo.fdcount()
print "Percent CPU %0.1f\n" % procinfo.cpuuse()
print "IO information %s\n" % procinfo.iostats()
print "Memory usage %s\n" % procinfo.memstats()
