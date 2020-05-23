# -*- coding: utf-8 -*-
from TorRequests.ConnectionManager import ConnectionManager

cm = ConnectionManager(5)
for j in range(100):
    for i in range(3):
        print(cm.request("http://icanhazip.com/").text.strip())
