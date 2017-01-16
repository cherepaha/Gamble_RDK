from psychopy import monitors
from constants import *

class MonitorSetup:   
    def setup_monitor(self):
        mon = monitors.Monitor(MONITOR, width=SCREENSIZE[0], distance=MONITOR_DISTANCE)
        mon.setSizePix(DISPSIZE)
        mon.saveMon()
        
ms = MonitorSetup()
ms.setup_monitor()