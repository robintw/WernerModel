import matplotlib.pyplot as plt
from scipy import io

a = io.loadmat("MLOutput300.mat")
g = a["Grid"]

plt.imshow(g)
c = plt.colorbar()
c.set_label("Number of Slabs")

plt.xlabel('Downwind Distance')

plt.savefig("ROutput.png", bbox_inches='tight')