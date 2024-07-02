Title: Change of variables integration from first principles
Date: 2024-05-15 12:30
Category: Math
Status: draft

we're going to develop an intuitive understanding of change of variables integration in single and multiple variables with the minimum formal mathematics required. I assume you already learned integration, so I will focus on developing a more intuitive understanding of it. We will start from the single variable case.

## The Definite Integral
Let $f$ be a real function of a real variable. We are interested in the area under it in some interval $[a,b]$. The direct way to approximate it is to divide the interval to $n$ segments of size $\Delta x$, and calcuate the sum
$$\sum_{i=1}^{n} f(x_i) \cdot \Delta x$$where $x_i$ is in the ith segment (could be the left, right or some other point). As $\Delta x \to 0$  this approximation gets closer to the actual area, and in fact the limit (when it exists) is what we define to be the integral, or the area under the curve.

This is all well and clear, so let's move on to a concrete example. Consider $f(x)=x^2$, which we want to integrate from 0 to 1, ie
$$\int_0^1 x^2dx$$
There are several approaches for calculating this integral. We will use change of variables even though it's needless here. 

As you learned in school, the process is to define a new variable $y= x^2$. Then we replace the differential $dy=2xdx $

SHOULD USE A DIFFERENT FUNCTION