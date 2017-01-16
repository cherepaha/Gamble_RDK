from __future__ import division
from psychopy import visual
import numpy as np

# This class implements ranom dot kinematogram (RDK) based on PsychoPy's ElementArrayStim
# using the algorithm of Shadlen & Newsome (2001). In a review paper by Pilly & Seitz (2009)
# this algorithm is labelled MN (Movshon/Newsome), hence the class name
class RDK_MN:   
    n_sequences = 3

    def __init__(self, psychopy_disp, density = 16.7, dot_speed = 5.0, 
                        frame_rate = 60, field_size = 5.0, field_scale = 1.1):
        self.dot_speed = dot_speed
        self.frame_rate = frame_rate
        self.field_size = field_size
        
        field_width = field_size*field_scale
        self.n_dots = int(np.ceil(density * field_width**2 / frame_rate))
        # due to ElementArrayStim limitations, n_dots has to be divisible by n_sequences
        # so we artificially add extra dots in case it isn't divisible 
        # (a couple of extra dots won't be a problem)
        self.n_dots += (self.n_sequences - self.n_dots % self.n_sequences) % self.n_sequences

        n_elements = self.n_dots/self.n_sequences
        if (n_elements * self.n_sequences != self.n_dots):
            raise ValueError('Check n_elements parameter provided to ElementArrayStim! ' 
                            'It should be equal to n_dots/self.n_sequences, where n_dots is '
                            'calculated based on density, frame rate and field width.')
            
        self.dot_stim = visual.ElementArrayStim(psychopy_disp, elementTex=None, 
                                                fieldShape='circle', elementMask='circle', 
                                                sizes=0.06, nElements = n_elements,
                                                units='deg', fieldSize = field_size)

    def initialize_rdk_stim(self, direction, coherence):
        self.direction = direction
        self.coherence = coherence
        
        # calculate dot displacement (in degrees of visual angle) per n_sequence frames
        displacement = (self.dot_speed/self.field_size) * self.n_sequences / self.frame_rate
        self.deltaX = displacement*np.cos(np.pi*self.direction/180.0)
        self.deltaY = displacement*np.sin(np.pi*self.direction/180.0)
        
        # stores logical index of the dots belonging to current sequence
        current_sequence_dots = np.zeros(self.n_dots, dtype=bool)            
        dot_positions = np.random.rand(2, self.n_dots)
        current_sequence = -1
        
        return current_sequence_dots, dot_positions, current_sequence
        
    def update_rdk_stim(self, current_sequence_dots, dot_positions, current_sequence):
        current_sequence = (current_sequence + 1) % self.n_sequences
        # first, set all values to False
        current_sequence_dots[current_sequence_dots] = False
        # second, set to True the values corresponding to the dots belonging to current sequence
        current_sequence_dots[current_sequence::self.n_sequences] = True
        
        # number of dots in the current frame, alternatively calculated as n_dots/n_sequences
        current_n_dots = sum(current_sequence_dots)
        
        coherent_dots = np.zeros(len(current_sequence_dots), dtype=bool)
        # for each dot in the current sequence, randomly determine on each frame whether 
        # the dot should be coherently or randomly moved
        # coherent_rand is set to True for those dots of the current frame 
        # which are coherently moved
        coherent_rand = np.random.rand(current_n_dots) < self.coherence
        n_coherent_dots = sum(coherent_rand)
        n_noncoherent_dots = current_n_dots - n_coherent_dots
        
        coherent_dots[current_sequence_dots] = coherent_rand
        
        non_coherent_dots = current_sequence_dots.copy()
        non_coherent_dots[coherent_dots] = False
                    
        dot_positions[0, coherent_dots] += self.deltaX
        dot_positions[1, coherent_dots] += self.deltaY
        
        # Move non-coherent dots to a random position so they flicker
        # rather than walk randomly (with random velocity)
        dot_positions[:, non_coherent_dots] = np.random.rand(2, n_noncoherent_dots)
        
        # if a dot goes outside the aperture, replace it randomly 
        # rather than move it to the opposite side
        out_dots = np.any((dot_positions < 0) | (dot_positions > 1), axis=0)
        dot_positions[:, out_dots] = np.random.rand(2, sum(out_dots))
        
        xys = ((dot_positions[:,current_sequence_dots]-0.5)*self.field_size).transpose()
        self.dot_stim.setXYs(xys)
        
        return current_sequence_dots, dot_positions, current_sequence