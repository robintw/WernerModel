from matplotlib.pyplot import *
import numpy as np

data_1000 = np.loadtxt(r'/Users/robin/Documents/University/COMP6023/Modelling Assignment/New Werner Model/Outputs_FromIridis/FullOutput/results1000.csv', skiprows=1, delimiter=",", usecols=(1, 2, 3, 4, 5, 6))
data_2000 = np.loadtxt(r'/Users/robin/Documents/University/COMP6023/Modelling Assignment/New Werner Model/Outputs_FromIridis/FullOutput/results2000.csv', skiprows=1, delimiter=",", usecols=(1, 2, 3, 4, 5, 6))


t_1000 = np.transpose(data_1000)
t_2000 = np.transpose(data_2000)

# Create the figure
figure(figsize=(10, 10))

subplots_adjust(hspace=0.3, wspace=0.3)

# Create a grid of 2 x 2
subplot(2, 2, 1)

# Plot number of dunes
plot(t_2000[0], t_2000[2], "r-")
ylabel('Number of dunes')
xlabel('Basin Volume')
axis(ymax=40, ymin=15)
title('Number of dunes')
#hold(True)
#plot(t_1000[0], t_1000[1], "r:")

# Plot mean length
subplot(2, 2, 2)
plot(t_2000[0], t_2000[3], "g-")
ylabel('Mean length')
xlabel('Basin Volume')
title('Mean Length')

# Plot total length
subplot(2, 2, 3)
plot(t_2000[0], t_2000[4], "b-")
ylabel('Total length')
xlabel('Basin Volume')
title('Total Length')

# Plot max length
subplot(2, 2, 4)
plot(t_2000[0], t_2000[5], "k-")
ylabel('Maximum length')
xlabel('Basin Volume')
title('Maximum Length')