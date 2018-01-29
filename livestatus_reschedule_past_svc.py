#!/usr/bin/env python

import socket
import datetime
import json
import time

socket_path = '/usr/local/nagios/var/rw/live'

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(socket_path)
s.send("GET services\nColumns: host_name description next_check\nFilter: active_checks_enabled = 1\nOutputFormat: json\nColumnHeaders: off\n")
s.shutdown(socket.SHUT_WR)
rawdata = s.makefile().read()
s.close()
data = json.loads(rawdata)

now = time.time()
now_past = time.time() - 300
now_futur = time.time() + 120

for item in data:
    if item[2] < now_past:
        #print('PB!: ' + item[0] + ' ' + item[1])
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(socket_path)
        s.send("COMMAND [" + str(now) + "] SCHEDULE_SVC_CHECK;" + item[0] + ";" + item[1] + ";" + str(now_futur) + "\nOutputFormat: json\nResponseHeader: fixed16\n\n");
        s.shutdown(socket.SHUT_WR)
        rawdata = s.makefile().read()
        s.close()
