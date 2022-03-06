Title: Measure Theory 1 - So why do we need \(\sigma\)-algebras?
Date: 2010-12-03 10:20
Category: Math

# Introduction 

Lately I've been brushing up on my *Measure Theory*. I took the course in my senior year, excited to finally learn the proper foundation for probability theory, but I was soon disappointed by what seemed to be as mostly an exercise in formality. Seeing as how I was also somewhat fatigued of studying at this point, I sufficed with passing the grade with a decent grade and promptly forgot everything I learned. After some time though, it started to irritate me that I went through all this trouble and yet I get nervous when I read about measures. Even from a course like topology whose majority of results I also forgot still contributed to me later. 

So, I finally set out on a refresher. I found a book, "Probability and Stochastics" by Erhan Çinlar, which purpoted to cover probabilty from a measure-theoretic perspective, along with a whole chapter devoted specifically to the those measure theory subjects relevant to probability. I read them quite dilligently, with some of the material still being familiar enough to be covered quickly, while later subjects required more deliberate effort. After a month or so, I felt I had good a solid grasp on the ideas, but still I felt a tinge of fear that soon it will all be forgotten again. That is why I have decided to write one or more posts about aspects that I find interesting to ponder, process and share with you. The first one happens to be about $\sigma$-algebras.

# What are $\sigma$-algebras?


# Why we need $\sigma$-algebras

Well, we don't actually need them all the time. When you work with discrete probability spaces/random variables, such as toin cosses, or even countable ones like the geometric distribution, you can evaluate the probability on every possible event. In fact, when teaching elementary probability the subject isn't even mentioned. It is only when we introduce continuous random variables that we need to start taking more care.

Consider the uniform probability measure $P$ on the interval $[0,1]$. We can define it on an event $A$ as
$$P(A)=\int_{A}1\cdot dx$$
We can infer from the definition some properties:
- Normalization: $P([0,1])=1$.
- Invariance under rigid motion: moving an event doesn't change it's probability. (expand)
- Finite additivity: If we have some disjoint collection of events $A_1,\dots, A_n$ then
$$P(\bigsqcup_{i=1}^n A_i)=\sum_{i=1}^n P(A_i)$$

And actually (substantiate) a stronger property holds, Countable additivity.

Now, we would like to build and use events such that a contradiction arises. From the properties of $\sigma$-algebras, we can already infer that a rather strange construction is required. 

We start by defining an equivalence relation on $\mathbb R$. We say that $x,y\in\mathbb R$ are equivalent, $x\sim y$, if their difference is rational, $x-y\in\mathbb Q$. So all the rational are equivalent. $\sqrt2$ is equivalent to $\sqrt2-1$, but $\pi$ and $\sqrt2$ are not (trivial to see?). An equivalence relation gives us a partition of $\mathbb R$ to equivalence classes. We build a set $N\subseteq [0,1)$ that contains exactly one representative from each equivalence class. More specificialy, for each $x$ we will have some $n\in N$ such that $x\sim n$. If you are not convinced that one exists, consider $x-\lfloor x\rfloor$. 
<!-- Still, to build such set, we need to "choose" a representative from each  -->
Next, we define for each rational number $q\in (0,1)\cap\mathbb Q$ the set
$$N_q=N+q\mod 1=\dots$$
**Lemma**: $N\cap N_q=\varnothing$.  
**Proof**: Let $n\in N\cap N_q$. Then $n\sim x$ for some $x$. On the otherhand, $n=n'+q$ and $n'\sim x'$. So
$$x=n+q_n=n'+q+q_n=x'+q_{n'}+q+q_n$$
meaning $x\sim x'$. From uniqueness of representative $n=n'\Rightarrow q=0,1$ which is a contradiction.

**Lemma**: $P(N)=P(N_q)$  
**Proof**: The $\mod 1$ is basically splitting to two disjoint parts and moving each of them rigidly.

**Lemma**: $\bigsqcup_{q\in[0,1)\cap\mathbb Q}N_q=[0,1)$  
**Proof**: From the last lemma the union is disjoint, and we get $\bigsqcup_{q\in[0,1)\cap\mathbb Q}N_q\subseteq [0,1)$ since each set is contained in the interval. For the other direction, let $x\in[0,1)$. There is some representative $n\in N$ equivalent to $x$, $x=n+q$. Since both are in $[0,1)$, $q\in(-1,1)$. If $q$ is positive, then $x=n+q\in N_q$. If $q$ is negative then $x=n+q=n+(q+1)-1\in N_{q+1}$. Either way, $x$ is in the union and hence we get equality.

Now we are ready to show a contradiction. The probability of $[0,1)$ should be 1. On the other hand
$$\begin{align*}
P([0,1)) &= P(\bigsqcup_{q\in[0,1)\cap\mathbb Q}N_q)\\
&=\sum_{q\in[0,1)\cap\mathbb Q}P(N_q)\\
&=\sum_{q\in[0,1)\cap\mathbb Q}P(N)\\
\end{align*}$$
So now we are in a pickle. If $P(N)=0$ then $P([0,1))=0$. But if $P(N)=c>0$ then $P([0,1))=\infty$. Tada!

## But maybe this is not relevant for probability measures?

## How rare are these sets, and the axiom of choice



## References
- [Raz Kupferman's notes on Measure Theory](http://www.ma.huji.ac.il/~razk/iWeb/My_Site/Teaching_files/Chapter1_1.pdf)