from scipy import io
import numpy as np
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename

 
 
if __name__ == '__main__':
    root=Tk()
    in_file = askopenfilename()
    out_file = asksaveasfilename()
    root.destroy()
    print in_file

    a = io.loadmat(in_file)
    g = a["Grid"]
    
    np.savetxt(out_file, g, fmt="%1d")