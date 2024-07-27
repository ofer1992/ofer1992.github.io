Title: Musings on the reparametrization trick
Date: 2024-07-27 15:45
Category: Math
Status: published

Reading the *variational autoencoder* chapter from the ["Understanding Deep Learning"](https://udlbook.github.io/udlbook/) book (which is available for free!). Not trivial, which is why I never got around to learning it, I guess. There are a lot of moving math parts to figure out. One of them is called "the reparametrization trick". So what is it about?

Let's say we have a distribution over a variable $x$ parametrized by $\theta$, $P(x;\theta)$, and we also have some differentiable function $f(x)$. We want to find $\theta^*$ that maximizes the expectation of $f$ over this distribution:
$$
\mathbb E_{P(x;\theta)}\left[f(x)\right]
$$
For simplicity, we assume everything is 1-d. Nowadays the solution is always gradient descent (or ascent in this case), so as a first step we'd like to calculate
$$
\frac{\partial}{\partial \theta}\mathbb E_{P(x;\theta)}\left[f(x)\right]
$$
Question: how do you differentiate a distribution? well, this is defined as
$$
\frac{\partial}{\partial \theta}\mathbb E_{P(x;\theta)}\left[f(x)\right]=
\frac{\partial}{\partial \theta}\int{P(x;\theta)}f(x)dx
$$
Can we switch the derivative and the integral? I've never been able to answer this confidently. It depends on [Leibniz's integral rule](https://en.wikipedia.org/wiki/Leibniz_integral_rule). Let's assume we can, and we get
$$
\int\frac{\partial}{\partial \theta}P(x;\theta)f(x)dx
$$
In practice this is almost never tractable, so we want to estimate it. We can use the following trick to convert it to an expectation and then use sampling to estimate it:
$$
\begin{align}
\int\frac{\partial}{\partial \theta}P(x;\theta)f(x)dx &=
\int\frac{{\partial P(x;\theta)}/{\partial \theta}}{P(x;\theta)}P(x;\theta)f(x)dx\\
&= \int\frac{\partial}{\partial \theta}\left[\log{P(x;\theta)}\right]P(x;\theta)f(x)dx\\
&= \mathbb E_{P(x;\theta)}\left[f(x)\frac{\partial}{\partial \theta}\log{P(x;\theta)} \right]
\end{align}
$$
The expression $\frac{\partial}{\partial \theta}\log{P(x;\theta)}$ is called the *score function* and is often denoted $s(x;\theta)$. To sum up what we did so far, we found the following relation
$$
\frac{\partial}{\partial \theta}\mathbb E_{P(x;\theta)}\left[f(x)\right]
= \mathbb E_{P(x;\theta)}\left[f(x)s(x;\theta)\right]
$$
which we can go on to estimate with sampling.

Well, the reparametrization trick takes another approach. Let's say we already estimated the expectation using sampling, ie we have $N$ samples $x_i\sim P(x;\theta$) (abuse of notation but I mean sampled according to this distribution), then we can approximate the expectation with
$$\mathbb E_{P(x;\theta)}\left[f(x)\right]\approx \frac{1}{N}\sum_{i}f(x_i)$$
What if we tried to differentiate that with respect to $\theta$? let's try using the chain rule:
$$\frac{\partial}{\partial \theta}\mathbb E_{P(x;\theta)}\left[f(x)\right]\approx
\frac{1}{N}\sum_{i}\frac{\partial}{\partial \theta}f(x_i)=
\frac{1}{N}\sum_{i}\frac{df}{dx}\frac{\partial x_{i}}{\partial \theta}(??)$$
What is $\frac{\partial x_i}{\partial \theta}$? $x_i$ depends on $\theta$ but in a stochastic manner. I don't know how to do this kind of derivative, though I know there's a thing called stochastic calculus. What else can we do? well, we can consider a special case: what if our random variable $x$ satisfied an identity
$$x=x_\theta(\varepsilon)$$
where $\varepsilon$ has some distribution that doesn't depend on $\theta$? for example, let's say $x\sim \mathcal N(\mu, \sigma^2)$ is normally distributed where $\theta=(\mu,\sigma)$. Another way to write $x$ would be
$$
x=\sigma\cdot\varepsilon + \mu
$$
Where $\varepsilon\sim\mathcal N(0,1)$. In this case the stochasticity of $x$ doesn't depend on the parameters and
$$
\frac{\partial x}{\partial \theta}=\frac{\partial\sigma}{\partial \theta}\varepsilon+\frac{\partial \mu}{\partial \theta}
$$
In general, we would have 
$$\frac{\partial x}{\partial \theta}=\frac{\partial x_\theta}{\partial\theta}(\varepsilon)$$
Putting it all together, we can estimate the gradient by sampling $N$ times from the independent distribution $\varepsilon_i$ and calculating
$$
\frac{\partial}{\partial \theta}\mathbb E_{P(x;\theta)}\left[f(x)\right]\approx
\frac{1}{N}\sum_{i}\frac{df}{dx_\theta}\frac{\partial x_\theta}{\partial \theta}(\varepsilon_i)
$$


