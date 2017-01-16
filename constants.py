SUBJ_ID = None
SESSION_NO = 1

ID_RANGE = [101, 999]

T_SIGNAL = 300

FIXATION_DURATION_RANGE = [700, 1000]
TIMESTEP = 10 # if not keyboard mode, this sets mouse sampling interval in msec

# Important: number of trials per block should be divisible by number of conditions (coherence values)
PRACTBLOCKNR = 0 # number of practice blocks
PRACTBLOCKSIZE = 50 # number of practice trials per block
RECBLOCKNR = 1 # number of recorded blocks
RECBLOCKSIZE = 5 # number of recorded trials per block

# EYETRACKER
# 'smi', 'eyelink' or 'dummy' 
# (NB: if DUMMYMODE is True, trackertype will be set to dummy automatically)
TRACKERTYPE = 'dummy' 
DUMMYMODE = True # False for gaze contingent display, True for dummy mode (using mouse or joystick)
#LOGFILENAME = 'eyedata' # logfilename, without path
#LOGFILE = LOGFILENAME[:] # .txt; adding path before logfilename is optional
EVENTDETECTION = 'native'

# DISPLAY
SCREENNR = 1 # number of the screen used for displaying experiment
MONITOR = 'hemtracker_monitor'
DISPTYPE = 'psychopy' # either 'psychopy' or 'pygame'
DISPSIZE = (1366,768) # canvas size
SCREENSIZE = (31., 18.) # physical display size in cm
MONITOR_DISTANCE = 60 # distance from eyes to monitor in cm
BGC = (0,0,0,255) # backgroundcolour
FGC = (255,255,255,255) # foregroundcolour
