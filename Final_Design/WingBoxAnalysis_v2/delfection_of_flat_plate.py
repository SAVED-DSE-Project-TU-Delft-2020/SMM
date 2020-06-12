import numpy as np

a = 0.3879 / 2
b = 5 * a
E = 50*10e8
t = 0.000625
q0 = 146

x = np.linspace(-a, a, 1000)
y = np.linspace(-b, b, 1000)
x, y = np.meshgrid(x,y)

q = q0 * np.sin()