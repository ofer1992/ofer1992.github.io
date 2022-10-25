Title: Adventures In Differential Equations I
Date: 2022-10-24 13:10
Category: Math
Status: published

# On the insanity of Differential Equations books
When one wishes to study the topic of Differential Equations, there is no shortage (and perhaps an overabundance) of books. Thus I was immediately confronted with a first difficulty: which book to pick? <!-- add something about difference from calculus? -->
After some googling and browsing through Reddit I settled on a book called "*A First Course in Ordinary Differential Equations*", as it seemed quite short and to the point. Soon enough though, I started running into some peculiarities.
I come from a Math background, so when I see things like
$$M(x)dx+N(y)dy=0$$
or
$$\frac{dx}{x}=-kdt$$ <!--long one-->

I get a stroke. As any math freshman will tell you (if he was successfully indoctrinated by his professors) $\frac{dy}{dx}$ is merely a form of notation for the derivative
$$\frac{dy}{dx}(x_0)=\lim_{x\to x_0}\frac{y(x)-y(x_0)}{x-x_0}$$
and is most certainly not a fraction. Or is it?

<!-- Something about history of differentials -->
Being already a couple of years out of school, I have seen some of the "apocryphal" interpretations and reinterpretations of calculus. For example, in later courses such as *Differential Geometry*, differential forms are introduced and given notation such as $dx$, $dy$. I don't expect readers of DE books, especially those coming from the engineering or natural science world, to be familiar with this material, so that seemed unlikely. Historically the derivative was defined by Leibniz in terms of these "differentials", which were infinitesimal mystical beings. Later the derivative was availed by Cauchy who defined it through the concept of the limit. The differential were regiven a purpose, by defining them through the derivative as $dy:\mathbb R^2\to \mathbb R$,
$$dy(x,dx)=f'(x)dx$$
which indeed restores an algebraic meaning to $\frac{dy}{dx}=f'(x)$. You might hope this solves all our difficulties, but we are immediately confronted with the "manipulation" of the formula $M(x)dx+N(y)dy=0$ into 
 $$\int M(x)dx+\int N(y)dy=0$$
Again the indoctrinated student yells "*The $dx$ in $\int\cdot dx$ is just a notational device!*".

I attempt to carry on without much hope, but soon I realize this book was not meant for me. On every page I see it written, in bold letters
<div align="center" style="font-size:30px;bold;">
For Physicists Only
</div>
And so, I shamefully slink away, looking for another book, this time one geared towards mathematicians, by *Coddington*. Now all is well defined, and the only price to pay is the use of complex numbers.

## P.S.
If you wish to read a comforting explanation, read this [wiki article](https://en.wikipedia.org/wiki/Separation_of_variables#Ordinary_differential_equations_(ODE)) which sheds some light on the matter.
