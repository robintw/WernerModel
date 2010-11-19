# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:39:18 2010

@author: -
"""
import matplotlib.pyplot as plt
from scipy import io
from os import *

rootdir = "/Users/robin/Documents/University/COMP6023/Modelling Assignment/New Werner Model/Outputs_FromIridis/Depth14/"

for subdir, dirs, files in os.walk(rootdir):
    for f in files:
        root, ext = os.path.splitext(f)  
        print ext
        
        orig_root = root
        
        joined_path = os.path.join(rootdir, f)
        root, ext = os.path.splitext(joined_path)
        out_name = root + ".png"
        print out_name
        if ext == ".mat" and orig_root[0] ==  "M" and os.path.exists(out_name) == False:
            print "Processing " + f
            a = io.loadmat(f)
            g = a["Grid"]
            
            plt.figure()
            plt.imshow(g)
            #c = plt.colorbar(orientation="horizontal", aspect=30)
            #c.set_label("Number of Slabs")
            
            plt.xlabel('Downwind Distance')
            
            
                
            
            plt.savefig(out_name, bbox_inches='tight')
            
            plt.close()