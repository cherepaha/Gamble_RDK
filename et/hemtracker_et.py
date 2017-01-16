from pygaze import eyetracker
from constants import *

# This class wraps eye-tracking functions of PyGaze
class HEMTrackerET:   
    def __init__(self, user_interface, subj_id):
        self.user_interface = user_interface
        data_file = '%s.edf' % (subj_id)
        self.tracker = eyetracker.EyeTracker(self.user_interface.disp, data_file=data_file)
    
    def calibrate(self):
        # TODO: instead of calling pygaze.calibrate, try using pylink.getEYELINK().doTrackerSetup()
        # look also at pylink.getEYELINK().enableAutoCalibration()
        self.user_interface.mouse.set_visible(False)
        self.tracker.calibrate()
        self.user_interface.mouse.set_visible(True)
    
    def sample(self):
        return self.tracker.sample()
    
    def pupil_size(self):
        return 0 if DUMMYMODE else self.tracker.pupil_size()
    
    def close(self):
        self.tracker.close()
                   
    def start_recording(self, start_message):                        
        self.tracker.start_recording()
        self.tracker.status_msg(start_message)
        self.tracker.log(start_message)
        
    def stop_recording(self):
        self.tracker.stop_recording()
        
    def correct_drift(self):
        if not DUMMYMODE:
            checked = False
            while not checked:
                self.user_interface.show_fixation_screen(time = 0)
                checked = self.tracker.drift_correction(fix_triggered=True)