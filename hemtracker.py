from pygaze import libtime
from constants import *
import random
import numpy as np
from ui.hemtracker_ui import HEMTrackerUI
from da.hemtracker_da import HEMTrackerDA
from et.hemtracker_et import HEMTrackerET

# HEMTracker (hand-eye movement tracker) class provides high-level functions controlling the flow 
# of the experiment. To run the experiment, just create the instance of the class and call run_exp()
class HEMTracker:
    rdk_directions = [0., 180.]
    rdk_coherence_values = [0.032, 0.064, 0.128, 0.256, 0.512]
                                                               
    exp_info = {}
    
    def __init__(self):
        self.user_interface = HEMTrackerUI()        
        self.data_access = HEMTrackerDA()
        self.eye_tracker = HEMTrackerET(user_interface=self.user_interface, 
                                 subj_id=self.data_access.exp_info['subj_id'])
        self.exp_info = self.data_access.exp_info
           
    def run_exp(self):
        libtime.expstart()
        self.user_interface.show_intro_screen()
        
        for block_no in range(1, PRACTBLOCKNR+1):
            self.run_block(SESSION_NO, block_no, PRACTBLOCKSIZE, is_practice = True)
        
        scores = []
        for block_no in range(PRACTBLOCKNR+1, PRACTBLOCKNR+RECBLOCKNR+1):
            score = self.run_block(SESSION_NO, block_no, RECBLOCKSIZE, is_practice = False)
            scores.append(score)
        self.user_interface.show_end_experiment_screen(scores)
        
        self.eye_tracker.close()
        self.user_interface.close()
        
    def run_block(self, session_number, block_number, block_size, is_practice = False):
        if (block_size % len(self.rdk_coherence_values) != 0):
            raise ValueError('Block size is not divisible by number of coherence levels!')
            
        print('start block %i' % block_number)
        self.eye_tracker.calibrate()
        self.user_interface.show_block_intro_screen(block_size, is_practice)

        # to make sure that there's equal number of trials for each coherence value,
        # instead of randomly selecting coherence at each trial, we prepare coherence values 
        # for the whole block and then randomly shuffle the list 
        random_coherence_values = np.repeat(np.array(self.rdk_coherence_values), 
                                     block_size/len(self.rdk_coherence_values), axis=0)
        random.shuffle(random_coherence_values)
        
        accumulated_points = 0
        for trial_no in range(1, block_size+1):
            response_dynamics_log, gamble_log, choice_info, accumulated_points = \
                            self.run_trial(session_number, block_number, trial_no, is_practice,
                                           coherence = random_coherence_values[trial_no-1],
                                            direction = random.choice(self.rdk_directions), 
                                            accumulated_points = accumulated_points)
            self.data_access.write_trial_log(response_dynamics_log, gamble_log, choice_info)
        self.user_interface.show_block_end_screen(is_practice, accumulated_points)
        
        return accumulated_points
            
    def run_trial(self, session_number, block_number, trial_number, is_practice = False, 
                  coherence=0.512, direction = 0.0, accumulated_points=0):
        trial_info = {'subj_id': self.exp_info['subj_id'],
                      'session_no': session_number, 
                      'block_no': block_number,
                      'trial_no': trial_number,
                      'is_practice': is_practice,
                      'direction': direction,
                      'coherence': coherence}
                      
        self.user_interface.show_ready_screen()
        self.user_interface.show_fixation_screen(random.uniform(FIXATION_DURATION_RANGE[0], 
                                                                FIXATION_DURATION_RANGE[1]))
        
        self.eye_tracker.start_recording(start_message = 'subject %s block %d trial %d' % 
                                            (self.exp_info['subj_id'], block_number, trial_number))
        
        response_dynamics_log, response, response_time = self.user_interface.show_stimulus_screen(
                                                                    trial_info=trial_info,
                                                                    tracker=self.eye_tracker)
        self.eye_tracker.stop_recording()
        self.eye_tracker.start_recording(start_message = 'subject %s block %d trial %d' % 
                                            (self.exp_info['subj_id'], block_number, trial_number))
        
        gamble_log, gamble_time, gamble_value = self.user_interface.show_gamble_screen(
                                                            trial_info=trial_info,
                                                            response=response,
                                                            tracker=self.eye_tracker)
        self.eye_tracker.stop_recording()
        
        is_correct = (response == trial_info['direction'])
        points_earned = gamble_value * (1 if is_correct else -1)
        accumulated_points += points_earned
        
        choice_info = [trial_info['subj_id'], trial_info['session_no'], trial_info['block_no'], 
                       trial_info['trial_no'], trial_info['is_practice'], trial_info['direction'], 
                        str(trial_info['coherence']), response, response_time, is_correct, 
                        gamble_value, gamble_time, points_earned]

        self.user_interface.show_feedback_screen(points_earned, accumulated_points) 

        # drift correction after every fifth trial
        if trial_number % 5 == 0:
            self.eye_tracker.correct_drift()
        
        self.user_interface.show_fixation_screen(300)
        
        return response_dynamics_log, gamble_log, choice_info, accumulated_points