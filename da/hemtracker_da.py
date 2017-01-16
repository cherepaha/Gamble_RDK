from constants import *
import random, csv
import numpy as np
from datetime import datetime
import os

# This class implements data access layer of HEMTracker (primarily, logging).
# All data outputs are stored in tab-delimited format in txt files in 'data' folder
class HEMTrackerDA:                                     
    # stubs for experiment-level variables
    exp_info = {}
    response_dynamics_log_file = ''
    gamble_log_file = ''       
    choice_log_file = ''
    
    def __init__(self):
        self.exp_info['subj_id'] = self.generate_subj_id()        
        self.exp_info['start_time'] = datetime.strftime(datetime.now(), '%b_%d_%Y_%H_%M_%S')
        self.initialize_log()
    
    def initialize_log(self):
        log_path = 'data/raw/%s/'        
        log_name = log_path + self.exp_info['subj_id'] + '_' + \
                self.exp_info['start_time'] + '_%s.txt'

        if not os.path.exists(log_path % 'choices'):
            os.makedirs(log_path % 'choices')
            
        self.choices_log_file = log_name % ('choices', 'choices')
        with open(self.choices_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'session_no', 'block_no', 'trial_no', 'is_practice', 
                             'direction', 'coherence', 'response', 'response_time', 'is_correct',
                             'gamble_value', 'gamble_time', 'points_earned'])

        if not os.path.exists(log_path % 'dynamics'):
            os.makedirs(log_path % 'dynamics')
        if not os.path.exists(log_path % 'gamble'):
            os.makedirs(log_path % 'gamble')
        
        self.response_dynamics_log_file = log_name % ('dynamics', 'dynamics')
        self.gamble_log_file = log_name % ('gamble', 'gamble')

        with open(self.response_dynamics_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'session_no', 'block_no', 'trial_no', 'timestamp', 
                             'mouse_x', 'mouse_y', 'eye_x', 'eye_y', 'pupil_size'])
        with open(self.gamble_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'session_no', 'block_no', 'trial_no', 'timestamp', 
                             'mouse_x', 'mouse_y', 'eye_x', 'eye_y', 'pupil_size'])

    def write_trial_log(self, response_dynamics_log, gamble_log, choice_info):            
        with open(self.choices_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(choice_info)        
            
        with open(self.response_dynamics_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerows(response_dynamics_log)
        
        with open(self.gamble_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerows(gamble_log)

    # this function generates new random subject id if one is not provided in constants.py
    # (which is only the case for experiments requiring multiple sessions with each subject)
    def generate_subj_id(self):
        if SUBJ_ID is None:
            existing_subj_ids = np.loadtxt('existing_subj_ids.txt')
            subj_id = int(random.uniform(ID_RANGE[0], ID_RANGE[1]))
            while subj_id in existing_subj_ids:
                subj_id = int(random.uniform(ID_RANGE[0], ID_RANGE[1]))
    
            with open('existing_subj_ids.txt', 'ab+') as fp:
                writer = csv.writer(fp, delimiter = '\t')
                writer.writerow([str(subj_id)])
        else:
            subj_id = SUBJ_ID
        return str(subj_id)