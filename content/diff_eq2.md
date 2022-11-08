Title: Adventures In Differential Equations II
Date: 2022-11-02 22:00
Category: Math
Status: draft

# Several outlooks on differential equations

## The algebraic perspective
The algebraic way to think about differential equations is perhaps the most familiar, as at least on first sight it might look like a regular equation with variables one encounters in his studies. We get an equation like
$$y''+y=0$$
or
$$y'=y^{\frac15}$$
where the variable $y$ really stands for a function, and $y'$ is the derivative etc. We might expect that some algebraic manipulations will reveal the answer, like often happens (or does it?) with regular equations.
<!-- After some manipulations one begins to lose hope -->

The technique of separation of variables (mentioned in the [previous post]({filename}diff_eq1.md)) belongs to this category. For example, the second equation can be solved by
$$\begin{align*}
y' &= y^\frac15\\
y^{-\frac15}y'&=1\\
\int y^{-\frac15}y'dx&=\int 1dx\\
\frac54y^\frac45+C &=x\\
y &=(\frac45x+C)^\frac54
\end{align*}$$
which only contains algebraic manipulations and calculus. While the algebraic perspective is straightforward, it doesn't tell the whole story, and it leaves us hanging dry when the equation is/seems insoluble.

## The geometric perspective
This perspective is very much the focus of the book *"Nonlinear Dynamics and Chaos"* by Steven Strogatz, at least the part I read so far (which is admittedly not much). Let's consider the equation
$$x''=-x$$

ALGEBRAIC SOLUTION?

Let's define a new variable $v=x'$. This transforms the second-order differential equation to a first-order system of two equations
$$\begin{align*}
x' &= v\\
v' &= -x
\end{align*}$$
We can imagine the $(x,v)$ plane.
<p style="width:50%; margin:auto">
  <img src="{static}images/diff_eq2/grid.png" />
</p>

These equations then define a vector field over the plane
$$f(x,v)=(v,-x)$$
We usually visualize vector fields by drawing arrows originating from points in the plane, with size indicating magnitude.
<p style="width:50%; margin:auto">
  <img src="{static}images/diff_eq2/vec_field.png" />
</p>

If we imagine a particle starting from some point on the plane, the vector field tells us where it will flow in the next moment. We can repeat this process and get a trajectory, or a curve, through the plane. Let's call it $\phi$. So $\phi$ is a function mapping time $t$ to the plane, and from how we "defined" it, the tangent to the curve at each point on the curve $(\phi_x(t),\phi_v(t))$ is $f(\phi_x(t),\phi_v(t))$. I claim that $\phi_x$, the first coordinate of the curve, is a solution to the differential equation:
<!-- $$\begin{align*}
\phi_x''&=\frac{d\phi_x}{d^2t}\\
&=\frac{d}{dt}\left(\frac{d\phi_x}{dt}\right)\\
&=\frac{d}{dt}\left(f_x(\phi_x,\phi_v)\right)\\
&=\frac{d}{dt}(\phi_v)\\
&=f_v(\phi_x,\phi_v)\\
&=-\phi_x\\
\end{align*}$$ -->

$$\begin{align*}
\phi_x''&=\left(\phi_x'\right)'\\
&=\left(f_x(\phi_x,\phi_v)\right)'\\
&=\phi_v'\\
&=f_v(\phi_x,\phi_v)\\
&=-\phi_x\\
\end{align*}$$
In fact, any curve that satisfies this property, that the tangent to the curve at a point is equal to the vector field at that point, is a solution to the differential equation. The beauty of this approach is that it is immediately clear from the picture of the vector field that solutions exist for every initial condition, and how the solution will look like (for example, that it oscillates). We can also read off qualitative properties, like stationary points.

Of course, existence of solutions (and uniqueness) requires a mathematical proof which is not trivial, but looking at the picture shows it to be plausible, whereas looking at the differential equation a-priori gives no clue to that question.

## The operator perspective
The most general definition of differential equation of order $n$ as an equation
$$f(t,x,x',\dots,x^{(n)})=0$$
where $f$ is smooth and a solution is a function $\phi$ that satisfies this equation
$$f(t,\phi,\phi',\dots,\phi^{(n)})=0$$
In the case of a linear differential equation then $f$ is a linear operator, which we can for convenience note as $L$. If we take the level of abstraction a bit higher, we can think of $L$ as linear operator on the vector space of smooth functions. For example, we can think of the equation $x''-x'+x=0$ as defining an operator $L(\phi)(t)=\phi''(t)-\phi'(t)+\phi(t)$ that maps $\phi$ to some new function $\psi$ so defined.  Then a solution to the differential equation is simply a function that maps to the zero function!

Now, in linear algebra we talk about the kernel of linear transformations, the set of vectors mapped to the zero vector, and the various cases where it is or is not trivial. To be honest, I don't know how much of that carries over to the case above, since some care is required (for example, the space of smooth functions is infinite-dimensional). Still, something to think about.