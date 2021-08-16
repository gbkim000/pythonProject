import numpy as np
from scipy import signal

# Make mine map
y, x = 5, 5
mine = np.zeros((y, x))

r = np.random.randint(0, y, 2)
c = np.random.randint(0, x, 2)

mine[r, c] = 1

# Fine mine
kernel = np.ones((3, 3))

result = signal.convolve2d(mine, kernel, 'same')
result[r, c] = 0

print mine
print result