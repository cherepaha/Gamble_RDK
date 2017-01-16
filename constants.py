# Set SUBJ_ID and SESSION_NO only if running multiple sessions for each subject
SUBJ_ID = None
SESSION_NO = 1

# Range of values for subject id
ID_RANGE = [101, 999]

# Time of warning sound signal (when subject doesn't move mouse from the starting position)
T_SIGNAL = 300

# Min and max duration of fixation display before RDK stimulus is shown
FIXATION_DURATION_RANGE = [700, 1000]

# Important: number of trials per block should be divisible by number of conditions (coherence values)
PRACTBLOCKNR = 0 # number of practice blocks
PRACTBLOCKSIZE = 5 # number of practice trials per block
RECBLOCKNR = 1 # number of recorded blocks
RECBLOCKSIZE = 5 # number of recorded trials per block

# EYETRACKER
# 'smi', 'eyelink' or 'dummy' 
# (NB: if DUMMYMODE is True, trackertype will be set to dummy automatically)
TRACKERTYPE = 'dummy' 
DUMMYMODE = True # False for gaze contingent display, True for dummy mode (using mouse or joystick)
EVENTDETECTION = 'native'

# DISPLAY
# Number of the screen used for displaying experiment (set to 0 if using one-monitor setup)
SCREENNR = 1
# Parameters for monitor_setup.py
MONITOR = 'hemtracker_monitor'
DISPTYPE = 'psychopy'
DISPSIZE = (1366,768) # canvas size in pixels
SCREENSIZE = (31., 18.) # physical display size in cm
MONITOR_DISTANCE = 60 # distance from eyes to monitor in cm
BGC = (0,0,0,255) # backgroundcolour
FGC = (255,255,255,255) # foregroundcolour
