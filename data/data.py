import json
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

from pprint import pprint
def readD(filename):
	with open(filename) as data_file:
		T = 1.00 / 800.0
		N = 50    
		data = json.load(data_file)
		x = np.array(data)
		yf = fft(x)
		xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
		plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
		plt.grid()
		plt.show()
		#print(y)

	#pprint(data)
readD('hi.json')