Title: AoC 2025 - Day 5
Date: 2025-12-04 11:13
Category: programming
Status: published

This one was quite easy, I quickly saw it can be solved by convolution but since I was using javascript I suffered with all the array handling and the for loops. After I finished the problem, I wanted to my hands on the python implementation, behold

```python
import numpy as np
from scipy import signal

with open("input.txt") as f:
  inp = f.read()
  
a = np.array([[1  if el == "@" else 0 for el in r] for r in inp.split()])
ker = np.array([[1,1,1],
				[1,0,1],
				[1,1,1]])

# part 2
inter = a.copy()
res = 0
while True:
  c = signal.convolve2d(inter, ker, mode='same')
  mask = (inter == 1) & (c < 4)
  s = mask.sum()
  if s == 0: break
  res += s
  inter[mask] = 0

print(res)
```

I guess sometimes array programming is the way.