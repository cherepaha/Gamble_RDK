from __future__ import division
from psychopy import visual
from pygaze import libscreen, libtime, libinput
import pygaze
from constants import *
import numpy as np
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound
from ui.rdk_mn import RDK_MN

# This class implements user interface of HEMTracker based on psychopy API (and partly pygaze)
class HEMTrackerUI:
    # TODO: Move all static elements (textboxes, etc.) to pure PsychoPy instead of PyGaze wrappers
    ready_button_size = (100, 40)
    ready_button_pos = (0, -DISPSIZE[1]/2 + ready_button_size[1]/2 + 30)

    response_button_size = (250, 250)
    response_button_pos_left = (-DISPSIZE[0]/2+response_button_size[0]/2, 
                                DISPSIZE[1]/2-response_button_size[1]/2)
    response_button_pos_right = (DISPSIZE[0]/2-response_button_size[0]/2, 
                                DISPSIZE[1]/2-response_button_size[1]/2)
    
    gambles = [10, 20, 30, 40, 50]
    gamble_button_size = (250, 60)

    def __init__(self):
        self.disp = libscreen.Display(monitor = MONITOR)
        self.mouse = libinput.Mouse(visible=True)
        self.keyboard = libinput.Keyboard(keylist=['space', 'left', 'right', 'lctrl', 'rctrl'], 
                                          timeout=None)

        self.blank_screen = libscreen.Screen()

        self.intro_screen = libscreen.Screen()

        self.intro_screen.draw_text(text='During each trial, a cloud of moving dots is going to \
                                            appear on the screen. Watch it carefully to detect \
                                            whether the dots in general are moving to the left or \
                                            to the right (click left mouse button to start)', 
                                            fontsize=18)
        
        self.fixation_screen = libscreen.Screen()
        self.fixation_screen.draw_fixation(fixtype='cross', pw=3)
        
        self.initialize_ready_screen()
        self.initialize_stimulus_screen()
        self.initialize_feedback_screen()
        
        self.warning_sound = sound.Sound(1000, secs=0.1)
    
    def initialize_ready_screen(self):
        self.ready_screen = libscreen.Screen()
        self.ready_screen.draw_text(text='Click the Start button to start the trial',  fontsize=18)

        self.ready_button = visual.Rect(win=pygaze.expdisplay, pos=self.ready_button_pos,
                                width=self.ready_button_size[0], 
                                height=self.ready_button_size[1],
                                lineColor=(200,200,200), lineWidth=3,
                                lineColorSpace='rgb255', fillColor=None)
        self.ready_button_text = visual.TextStim(win=pygaze.expdisplay, text='Start',
                                             pos=self.ready_button_pos, height=18)
        self.ready_screen.screen.append(self.ready_button)
        self.ready_screen.screen.append(self.ready_button_text)
    
    def initialize_stimulus_screen(self):
        self.stimuli_screen = libscreen.Screen()
        self.rdk = RDK_MN(pygaze.expdisplay)

        self.stimuli_screen.screen.append(self.rdk.dot_stim)
        
        self.left_response_image = visual.ImageStim(win=pygaze.expdisplay, 
                                                image='resources/images/arrow_left_sq.png', 
                                                pos=self.response_button_pos_left)        
        self.left_response_rect = visual.Rect(win=pygaze.expdisplay, 
                                pos=self.response_button_pos_left,
                                width=self.response_button_size[0], 
                                height=self.response_button_size[1],
                                lineColor=(5,5,5), lineColorSpace='rgb255', 
                                fillColor=None)
        
        self.right_response_image = visual.ImageStim(win=pygaze.expdisplay, 
                                                image='resources/images/arrow_right_sq.png', 
                                                pos=self.response_button_pos_right)        
        self.right_response_rect = visual.Rect(win=pygaze.expdisplay,
                                pos=self.response_button_pos_right,
                                width=self.response_button_size[0],
                                height=self.response_button_size[1],
                                lineColor=(5,5,5), lineColorSpace='rgb255', 
                                fillColor=None)
        
        self.stimuli_screen.screen.append(self.left_response_image)
        self.stimuli_screen.screen.append(self.left_response_rect)
        self.stimuli_screen.screen.append(self.right_response_image)
        self.stimuli_screen.screen.append(self.right_response_rect)

    def initialize_gamble_screen(self, loc='left'):
        response_button_pos = (self.response_button_pos_right if loc=='right' 
                               else self.response_button_pos_left)
        img = self.right_response_image if loc=='right' else self.left_response_image
        
        self.gamble_screen = libscreen.Screen()
        self.gamble_screen.screen.append(img)
        self.gamble_rects = []
        for i, gamble in enumerate(self.gambles):
            pos=(response_button_pos[0], response_button_pos[1]-self.response_button_size[1]/2 - \
                                                    (i+0.5)*self.gamble_button_size[1])
            rect = visual.Rect(win=pygaze.expdisplay, pos=pos,
                               width=self.gamble_button_size[0], height=self.gamble_button_size[1],
                                lineColor=(5,5,5), lineColorSpace='rgb255', 
                                fillColor=(255, 250, 250), fillColorSpace='rgb255')
            text = visual.TextStim(win=pygaze.expdisplay, pos=pos, text=gamble, height=36, 
                                   color=(5,5,5), colorSpace='rgb255')
            
            self.gamble_screen.screen.append(rect)
            self.gamble_screen.screen.append(text)
            self.gamble_rects.append(rect)
    
    def initialize_feedback_screen(self):   
        self.feedback_screen = libscreen.Screen()
        self.feedback_text = visual.TextStim(win=pygaze.expdisplay, 
                                             colorSpace='rgb255', height = 36)
        self.feedback_points_earned = visual.TextStim(win=pygaze.expdisplay, 
                                               pos = (0, -100), colorSpace='rgb255', height = 36)
        self.feedback_accumulated_points = visual.TextStim(win=pygaze.expdisplay, 
                                               pos = (0, -175), height = 36)
        
        self.feedback_screen.screen.append(self.feedback_text)
        self.feedback_screen.screen.append(self.feedback_points_earned)
        self.feedback_screen.screen.append(self.feedback_accumulated_points)
    
    def close(self):
        self.disp.close()
    
    def show_intro_screen(self):
        self.mouse.set_visible(True)
        self.disp.fill(self.intro_screen)
        self.disp.show()
        self.mouse.get_clicked()
        libtime.pause(300)
        
    def show_block_intro_screen(self, block_size, is_practice):
        self.mouse.set_visible(True)
        self.block_intro_screen = libscreen.Screen()
        block_type = 'practice' if is_practice else 'recorded'
        self.block_intro_screen.draw_text(text='You are about to start the block of %d %s trials.\
                                    To start click left mouse button.' % (block_size, block_type), 
                                    fontsize=18)
        self.disp.fill(self.block_intro_screen)
        self.disp.show()
        self.mouse.get_clicked()
        libtime.pause(200)
        
    def show_block_end_screen(self, is_practice, accumulated_points):
        self.mouse.set_visible(True)
        self.block_end_screen = libscreen.Screen()
        block_end_text = \
            '''You have completed this experimental block. \nYour score is %i points.
            \nClick left mouse button to proceed.''' % (accumulated_points)                
            
        self.block_end_screen.draw_text(text=block_end_text, fontsize=18)
        self.disp.fill(self.block_end_screen)
        self.disp.show()
        self.mouse.get_clicked()
        libtime.pause(200)
        
    def show_end_experiment_screen(self, scores):
        self.mouse.set_visible(True)
        self.experiment_end_screen = libscreen.Screen()
        experiment_end_text = \
            '''Congratulations! You have completed the experiment.
            Your scores for each block are displayed below. 
            \nClick left mouse button to proceed \n\n'''
        
        for i, score in enumerate(scores):
            experiment_end_text += 'Block %i: %i points \n' % (i+1, score)              
        self.experiment_end_screen.draw_text(text=experiment_end_text, fontsize=18)
        self.disp.fill(self.experiment_end_screen)
        self.disp.show()
        self.mouse.get_clicked()        
        
    def show_ready_screen(self):
        self.mouse.set_visible(True)
        self.disp.fill(self.ready_screen)
        self.disp.show()
        
        while not self.mouse.mouse.isPressedIn(self.ready_button):
            continue   
                        
    def show_fixation_screen(self, time = 0):
        self.mouse.set_visible(False)
        self.disp.fill(self.fixation_screen)
        self.disp.show()
        libtime.pause(time)
        
    def show_stimulus_screen(self, trial_info, tracker):
        self.mouse.set_visible(True)
        current_sequence_dots, dot_positions, current_sequence = \
            self.rdk.initialize_rdk_stim(trial_info['direction'], trial_info['coherence'])
        
        response_dynamics_log = []
        response = None
        
        stim_start_time = libtime.get_time()
        t = 0
        signal_played = False
        
        while response is None:
            if self.ready_button.contains(self.mouse.mouse) and t>T_SIGNAL and not signal_played:
                self.warning_sound.play()
                signal_played = True
                
            current_sequence_dots, dot_positions, current_sequence = \
                self.rdk.update_rdk_stim(current_sequence_dots, dot_positions, current_sequence)
            
            self.disp.fill(screen=self.stimuli_screen)            
            self.disp.show()
            
            # collect mouse and eye tracker samples
            t = libtime.get_time() - stim_start_time
            mouse_position = self.mouse.get_pos()
            eye_position = tracker.sample()
            pupil_size = tracker.pupil_size()
            
            response_dynamics_log.append([trial_info['subj_id'], trial_info['session_no'], 
                                     trial_info['block_no'], 
                                     trial_info['trial_no'], str(t), mouse_position[0], 
                                     mouse_position[1], eye_position[0], 
                                     eye_position[1], pupil_size])
            
            if self.mouse.mouse.isPressedIn(self.left_response_rect):
                response = 180
            elif self.mouse.mouse.isPressedIn(self.right_response_rect):
                response = 0
        
        return response_dynamics_log, response, t
        
    def show_gamble_screen(self, trial_info, response, tracker):
        self.mouse.set_visible(True)
        
        gamble_log = []
        gamble_value = None
        gamble_start_time = libtime.get_time()
        
        loc = 'right' if response == 0 else 'left'
        self.initialize_gamble_screen(loc)
        
        while gamble_value is None:
            self.disp.fill(self.gamble_screen)
            self.disp.show()
            
            t = libtime.get_time() - gamble_start_time
            mouse_position = self.mouse.get_pos()
            eye_position = tracker.sample()
            pupil_size = tracker.pupil_size()
            
            gamble_log.append([trial_info['subj_id'], trial_info['session_no'], 
                               trial_info['block_no'], trial_info['trial_no'], 
                                str(t), mouse_position[0], mouse_position[1], 
                                eye_position[0], eye_position[1], pupil_size])
            
            for i, gamble in enumerate(self.gambles):
                if self.mouse.mouse.isPressedIn(self.gamble_rects[i]):
                    gamble_value = gamble
        
        return gamble_log, t, gamble_value
    
    def show_feedback_screen(self, points_earned, accumulated_points):       
        self.mouse.set_visible(True)
        points_earned_str = '%i points'
        if points_earned > 0:
            self.feedback_text.setText('Correct!')
            self.feedback_text.setColor((52,201,64))
            self.feedback_points_earned.setColor((52,201,64))
            points_earned_str = '+' + points_earned_str
        elif points_earned < 0:
            self.feedback_text.setText('Incorrect!')
            self.feedback_text.setColor((196,46,46))
            self.feedback_points_earned.setColor((196,46,46))
            
        self.feedback_points_earned.setText(points_earned_str % (points_earned))
        self.feedback_accumulated_points.setText('Accumulated points: %i' % (accumulated_points))
        self.disp.fill(self.feedback_screen)
        self.disp.show()
        libtime.pause(500)
        self.mouse.get_clicked()