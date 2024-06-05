import matplotlib.pyplot as plt
import numpy as np

Ac = 1
xc = 1

X = np.linspace(1,40,100)
def f(x):
     return Ac*(1+2*((x-xc)/xc)**2)

plt.plot(X,500+f(X), color = 'b')
plt.plot(X,-500-f(X), color = 'b')
plt.show()