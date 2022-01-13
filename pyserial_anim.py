import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial


def set_ax1(fig):
    ax1 = fig.add_subplot(311)
    line1_water, = ax1.plot([], [],label='water')
    line1_oil, = ax1.plot([], [],label='oil')
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5,1.6))
    ax1.set_ylim(0,105)
    ax1.set_ylabel("light intensity (%)")
    ax1.set_xlabel('total time elapsed (s)')
    return ax1, line1_water, line1_oil

def set_ax2(fig):
    ax2 = fig.add_subplot(312)
    line2_water, = ax2.plot([],[])
    line2_oil, = ax2.plot([],[])
    ax2.set_ylim(0,105)
    ax2.set_ylabel("light intensity (%)")
    ax2.set_xlabel("last 10 seconds")
    return ax2, line2_water, line2_oil

def set_ax3(fig):
    ax3 = fig.add_subplot(313, sharex=ax2)
    line3_water, = ax3.plot([],[])
    line3_oil, = ax3.plot([],[])
    ax3.set_ylim(0,50)
    ax3.set_ylabel('RSD')
    ax3.set_xlabel("last 10 seconds")
    return ax3, line3_water, line3_oil


def animate(frame):
    # Read serial data
    ser = serial.Serial('COM3',9600)
    ser.close()
    ser.open()
    t.append(time.time()-t0)
    try:
        data = ser.readline().decode()[:-2]
    except ValueError:
        pass
    try:
        water_data.append(int(data.split(",")[0])*100/1020)
    except ValueError:
        water_data.append(water_data[-1])
    #Sometimes a IndexError occurs because the serial sends only first data,
    # hence a list index data.split(",")[1] out of range.
    try:
        oil_data.append(int(data.split(",")[1])*100/1020)
    except IndexError:
        oil_data.append(oil_data[-1])

    ser.close()


    # Plot data on ax1
    line1_water.set_data(t, water_data)
    line1_oil.set_data(t, oil_data)
    ax1.set_xlim(0,t[-1])

    # Plot data on ax2 and ax3
    line2_water.set_data(t,water_data)
    line2_oil.set_data(t,oil_data)

    if len(t)>170: #ie after 10 seconds (interval between two points is ill-defined)
        ax2.set_xlim(t[-170],t[-1])
    else:
        ax2.set_xlim(0,t[-1])

    if len(t)>10: #standard deviation calculation requires several datapoints
        water_rsd.append(100*np.std(water_data[-10:]/np.mean(water_data[-10:])))
        oil_rsd.append(100*np.std(oil_data[-10:]/np.mean(oil_data[-10:])))
        line3_water.set_data(t[10:],water_rsd)
        line3_oil.set_data(t[10:],oil_rsd)

    return ax1, ax2, ax3

if __name__ == '__main__':
    #lists initialisation
    t = list()
    water_data = list()
    oil_data = list()
    water_rsd = list()
    oil_rsd = list()

    #Set the display of the graphs
    fig = plt.figure()
    ax1, line1_water, line1_oil = set_ax1(fig)
    ax2, line2_water, line2_oil = set_ax2(fig)
    ax3, line3_water, line3_oil = set_ax3(fig)
    fig.subplots_adjust(hspace=0.5)

    #Timed animation loop
    t0 = time.time()
    ani = animation.FuncAnimation(fig, animate, frames=None, blit=False, interval=25, repeat=True)
    fig.show()