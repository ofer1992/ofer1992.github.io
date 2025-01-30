Title: Visualizing Lissajous curves with p5.js
Date: 2025-01-30 16:25
Category: Programming
Status: published

I've been continuing on my learning physics quests, currently alternating between electromagnetics and waves. I was reading chapter 2 of French's "Vibrations and Waves" and he talked there about Lissajous curves.

<p style="width:50%; margin:auto">
<img src="{static}images/lissajous_curves.png" />
</p>

These are 2d curves whose x-y coordinates are parametrized by cosines, ie
$$
\begin{align}
x&=A_x\cos (\omega_x t)\\
y&=A_y\cos(\omega_y t+\phi)
\end{align}
$$
We can deduce that the curves are bounded in a rectangle of sides $2A_x, 2A_y$. In general for arbitrary frequencies, the curves can be quite chaotic and infact it can be shown that if the frequencies don't satisfy a kind of integer relationship
$$n_x A_x =n_y A_y$$
then the curves never repeat themselves. When the frequencies have simple integer ratios though, the curves can be quite aesthetic, as seen in the image above.

In the book they have this cool figure,

And I figured (no pun intended) it would be fun to write an interactive version. I figured `p5.js`, which is a neat javascript library could handle this. I even found [this](https://p5js.org/examples/angles-and-motion-sine-cosine/) example which gave me a really convenient starting point.

So, Without further ado, 

<iframe  width="650" height="850" src="https://ofer1992.github.io/tools/lissajous/">