import numpy as np
import matplotlib.pyplot as plt
from scipy import io
import math
from operator import itemgetter
from random import choice
import time

class werner:
    """Contains methods for running the Werner (1995) model of sand dune evolution"""
    x_len = 0
    y_len = 0

    slab_ratio = 0.1
    
    num_iterations = 0
    jump_length = 0
    
    pd_s = 0
    pd_ns = 0
    
    # Grid variable
    grid = 0
    
    altered = False
    depth = 0
    
    # Shadow map
    shadow_map = 0
    
    # Iteration number
    it_num = 0
    
    # Avalanche counts per iteration
    av_count = 0
    
    def run(self, y, x, initial_value, num_its, altered):
        """Run the model with the arguments: y_length, x_length, initial_value, number_of_iterations, altered"""
        self.initialise_grid(y, x, initial_value)
        
        self.write_file()
        
        self.initialise_shadow_map()
        
        self.num_iterations = num_its
        
        # Standard parameter values
        self.jump_length = 1
        self.pd_s = 0.6
        self.pd_ns = 0.4
        
        self.altered = altered
        
        if self.altered == True:
            # Create the depth grid
            self.depth = np.zeros( (y, x) )
            
            # Set the main depression
            self.depth[:, range(110, 191)] = -10
            
            # Run down to it
            self.depth[:, 109] = -9
            self.depth[:, 108] = -8
            self.depth[:, 107] = -7
            self.depth[:, 106] = -6
            self.depth[:, 105] = -5
            self.depth[:, 104] = -4
            self.depth[:, 103] = -3
            self.depth[:, 102] = -2
            self.depth[:, 101] = -1
            
            # Run up from it
            self.depth[:, 191] = -9
            self.depth[:, 192] = -8
            self.depth[:, 193] = -7
            self.depth[:, 194] = -6
            self.depth[:, 195] = -5
            self.depth[:, 196] = -4
            self.depth[:, 197] = -3
            self.depth[:, 198] = -2
            self.depth[:, 199] = -1
            
        
        self.avcount = np.zeros(num_its + 1)
        
        # Run the model
        self.main_loop()
        
        print self.avcount
        io.savemat("Counts.mat", { "count":self.avcount})
        np.save("Counts.npy", self.avcount)
    
    def run_std(self):
        """Runs the Werner (1995) CA model of sand dunes"""
        print "Initialising grid"
        self.initialise_grid(50, 100, 3)
        
        self.initialise_shadow_map()
        
        self.num_iterations = 100
        self.jump_length = 1
        
        self.pd_s = 0.6
        self.pd_ns = 0.4
        
        self.avcount = np.zeros(self.num_iterations + 1)
        
        
        before = time.time()
        self.main_loop()
        after = time.time()
        
        time_taken = after - before
        
        print "Took %f% seconds", time_taken
        
    def main_loop(self):
        """Runs the main loop of the Werner model"""
        for iteration in xrange(1, self.num_iterations + 1):
            print "At iteration %d" % iteration
            self.it_num = iteration
            
            ### Select cells randomly without replacement
            x, y = np.meshgrid(np.arange(self.x_len), np.arange(self.y_len))
    
            x = x.flat
            y = y.flat
            
            shuffled_indices = np.random.permutation(np.arange(self.x_len * self.y_len))
            
            for index in shuffled_indices:
                # Get the current y and x indices
                cur_y, cur_x = y[index], x[index]
                
                
                if self.altered == False:
                    # Use the standard version
                    if self.grid[cur_y, cur_x] == 0:
                       # If there's no slab there then we can't erode it!
                       continue
                else:
                    # Use the altered version of checking if we can erde
                    if self.grid[cur_y, cur_x] == self.depth[cur_y, cur_x]:
                        # We can't erode it, so continue
                        continue
    
                
                #if cur_x >= 100 and cur_x <= 200:
                #    pass
                #elif self.grid[cur_y, cur_x] == 0:
                #    # If there's no slab there then we can't erode it!
                #    continue
                
                # Check to see if the cell is in shadow.
                if self.cell_in_shadow(cur_y, cur_x):
                    # If it's in shadow then we can't erode it, so go to the next random cell                    
                    continue
                
                ## TODO: Fix probability of erosion stuff below
                if True:
                    # Move a slab
                    self.grid[cur_y, cur_x] -= 1
                    
                    orig_y, orig_x = cur_y, cur_x
                    
                    # Loop forever - until we break out of it
                    while True:
                        new_y, new_x = cur_y, self.add_x(cur_x, self.jump_length)
                        
                        if self.grid[new_y, new_x] == 0:
                            prob = self.pd_ns
                        else:
                            prob = self.pd_s
                        
                        if np.random.random_sample() <= prob:
                            # Drop cell
                            break
                        else:
                            cur_y, cur_x = new_y, new_x
                    
                #print "Dropping on cell"
                #print new_y, new_x
                # Drop the slab on the cell we've got to
                self.grid[new_y, new_x] += 1
                
                self.do_repose(orig_y, orig_x)
                
                self.do_repose(new_y, new_x)
                
            self.write_file()
            
    def calc_locations(self, y, x):
        """Calculates the locations of the four cardinal direction cells from the current cell: B, H, D, and F"""
        # A  B  C
        # D  *  F
        # G  H  I
        
        locs = {}
    
        locs['B'] = {'y': self.add_y(y, -1), 'x':x}
        locs['H'] = {'y': self.add_y(y, 1),  'x':x}
        locs['D'] = {'y': y,            'x': self.add_x(x, -1)}
        locs['F'] = {'y': y,            'x': self.add_x(x, 1)}
    
        return locs
        
    def diff(self, val1, val2):
        """Returns the difference between the two heights"""    
        result = abs((val1 * self.slab_ratio) - (val2 * self.slab_ratio))
    
        if val1 < val2:
            # Upwards angle
            flag = 1
        elif val1 > val2:
            # Downwards angle
            flag = -1
        else:
            flag = 0
        return [result, flag]
        
    def calc_diffs(self, y, x, locs):
        """Calculates the differences between the given cell and its neighbours"""
        res = {}
        
        for item, value in locs.iteritems():
            res[item] = self.diff(self.grid[y, x], self.grid[value['y'], value['x']])
    
        return res
        
    def avalanche_slab(self, from_y, from_x, to_y, to_x):
        """Avalanche a slab from from_y, from_x to to_y, to_x"""
        self.grid[from_y, from_x] -= 1
        self.grid[to_y, to_x] += 1
        
        self.avcount[self.it_num] += 1
        
        
                
    def do_repose(self, y, x):
        """Check the angle of repose on a cell and avalanche if needed"""
        
        #print "In do_repose"
        #print y, x       
        
        locs = self.calc_locations(y, x)
        diffs = self.calc_diffs(y, x, locs)
        
        abs_diffs = {}
        
        # Get te absolute values of all of the diffs
        for item, value in diffs.iteritems():
            abs_diffs[item] = abs(value)

        
        just_right_dirs = [diff for diff in diffs.items() if diff[1][0] > 0.5 and diff[1][1] != 0]
        
        if len(just_right_dirs) == 0:
            # No steep angles in the right direction, so exit
            return
        
        # Sort the diffs (largest at the top)
        s = sorted(dict(just_right_dirs).items(), key=itemgetter(1), reverse=True)
        
        if s[0][0] < 0.5:
            # No angles too steep
            print "SHOULDN'T GET HERE"
            raw_input("HELP: Press enter")
            return
        
        # Filter the list to get just the items that are the same as the item at the top (TODO: Check for floating point error?)
        filtered = [item for item in s if item[1] == s[0][1]]

        # Assuming we've actually got something left...        
        if filtered:
            # Select one randomly
            chosen = choice(filtered)
    
            # Get the direction of our choice
            chosen_dir = chosen[0]
            
            if chosen[1][1] == -1:
                #print "Avalanching to the direction"
                # Avalanche from the direction we've chosen
                from_y, from_x = y, x
                to_y, to_x = locs[chosen_dir]['y'], locs[chosen_dir]['x']
    
                # Do the avalanching
                self.avalanche_slab(from_y, from_x, to_y, to_x)
    
                self.do_repose(to_y, to_x)
            elif chosen[1][1] == 1:
                #print "Avalanching from the direction"
                # Avalanche to the direction we've chosen
                from_y, from_x = locs[chosen_dir]['y'], locs[chosen_dir]['x']
                to_y, to_x = y, x
    
                # Do the avalanching
                self.avalanche_slab(from_y, from_x, to_y, to_x)
    
                self.do_repose(from_y, from_x) 
        
    def cell_in_shadow(self, y, x):
        """Determines whether a cell is in shadow or not"""
        orig_x = x
        orig_value = self.grid[y, orig_x]
        
        # Move to the left
        x = self.add_x(orig_x, -1)
        
        max_in_row = self.grid[y].max()
        
        while x != orig_x:
            # Get the height difference that's needed from the shadow map
            height_needed = self.shadow_map[ (orig_x - x) % self.x_len]
            if self.grid[y, x] - orig_value >= height_needed:
                return True
            elif orig_value + height_needed > max_in_row:
                return False
            
            x = self.add_x(x, -1)
        
        return False
        
        
    def initialise_shadow_map(self):
        """Initialises the shadow map using integers"""
        self.shadow_map = np.zeros( self.x_len + 1, np.int8)
        
        for i in range(1, self.x_len + 1):
            self.shadow_map[i] = int((math.tan(math.radians(15)) * i) * (1 / self.slab_ratio))

    
    def initialise_grid(self, y, x, starting_value):
        """Initialise a grid of the size x by y, setting all cells to
        the starting value"""
        # Create a grid of the specified size
        self.grid = np.zeros( (y, x), np.int8, 'C')
        
        # Record the sizes in the class variables
        self.x_len = x
        self.y_len = y
        
        # Set the initial values of the array
        self.grid += starting_value
        
    def write_file(self):
        """Writes out files showing the grid"""
        if self.it_num % 5 == 0:
            plt.imshow(self.grid)
            plt.savefig("output%.4d.png" % self.it_num)
            io.savemat("MLOutput%.4d" % self.it_num, { "Grid":self.grid})
    
    def add_x(self, x, add):
        """Adds a value to an x co-ordinate in clock-face (modular) arithmetic
        using the x_len specified in the class"""
        return (x + add) % self.x_len
        
    def add_y(self, y, add):
        """Adds a value to an y co-ordinate in clock-face (modular) arithmetic
        using the y_len specified in the class"""
        return (y + add) % self.y_len
    
    
