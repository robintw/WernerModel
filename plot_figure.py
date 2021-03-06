import matplotlib.pyplot as plt
from scipy import io
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
    
    plt.figure()
   # plt.imshow(g, vmin=-12, vmax=20)
    plt.imshow(g)
    #c = plt.colorbar(orientation="horizontal", aspect=30)
    c = plt.colorbar()
    c.set_label("Number of Slabs")
    
    plt.xlabel('Downwind Distance')
    
    plt.savefig(out_file, bbox_inches='tight')
    