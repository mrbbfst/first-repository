import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()

ax.plot(x, y)
ax.set_xlabel('x')

plt.show()