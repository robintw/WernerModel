from matplotlib.pyplot import *
import numpy as np

data5 = np.load("DepthGrid5.npy")
data10 = np.load("DepthGrid10.npy")

figure()


plot(np.zeros( (500) ), "k-", label="0")
hold(True)

plot(data5[0], "r--", label="5")
hold(True)


plot(data10[0], "r-", label="10")
axis(ymin=-15, ymax=5)

xlabel('Downwind Distance')
ylabel('Maximum Depth ($d_{min}$)')


legend()