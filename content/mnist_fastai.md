Title: Building up PyTorch abstractions: Part 1
Date: 2024-07-28 18:01
Category: Dailies
Status: published
Today we will retrace lesson [13](https://www.youtube.com/watch?v=vGdB4eI4KBs)-[14](https://www.youtube.com/watch?v=veqj0DsZSXU)'s notebook that "builds up" pytorch abstractions from scratch. As a first step we'll rederive everything in hardcore numpy (maybe hardcore should be reserved for C). Then we'll start building the abstractions.

First up we load `mnist` data:

```python
from pathlib import Path
from fastdownload import FastDownload # nice helper for caching downloads
import gzip, pickle

MNIST_URL='https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/data/mnist.pkl.gz?raw=true'
path_gz = FastDownload().download(MNIST_URL)

with gzip.open(path_gz, 'rb') as f:
	((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding='latin-1')
```

### Forward pass
We'll build a simple MLP with one hidden layer:

```python
dim_in = x_train.shape[1]
dim_h = 50
dim_out = max(y_train) + 1

W1 = np.random.randn(dim_h, dim_in)
b1 = np.random.randn(dim_h)
W2 = np.random.randn(dim_out, dim_h)
b2 = np.random.randn(dim_out)

# Linear layer op
def lin(x, W, b):
  return x @ W.T + b

x = x_train[:50]
h = lin(x, W1, b1).clip(min=0)
out = lin(h, W2, b2)
y_pred =  out.argmax(axis=1)
```
Weight initialization is something easy to forget about, as it is done by pytorch behind the scenes anytime you initialize a layer with parameters. Here we just use normal distribution. The net isn't deep so we won't have any trouble. `out` contains the unnormalized logits of the predictions, and `y_pred` the predicted labels.

To calculate the loss we use the cross-entropy, or negative log-likelihood when using labels:
```python
loss = -(out - logsumexp(out, 1))[range(bs), y].mean()
```

### Backward pass
After the forward pass we have to backpropagate the gradient. Let's start with `dout`. To simplify our life we ignore the batches. Something about calculating gradients in neural networks can be really confusing. I think the way to do it is first to mark the right intermediate outputs as variables, and when calculating gradient of loss with respect to a var, use chain rule separately for each function/variable that depends on that var and add it all up.

#### Loss function
The loss is for a sample $(x,y)$ is
$$
l=-\log p_y
$$
where $p$ is the predicted probability for label $y$. Then,
$$\frac{\partial l}{\partial \log p_i}=\begin{cases}
-1 && i=y
\\
0 && i\neq y
\end{cases}
$$
Some care is needed as `out` holds the unnormalized logits. From the code we see that
$$
\log p_i = out_i - \log\sum_ke^{out_k}
$$
and so
$$
\frac{\partial \log p_i}{\partial out_j}=
\begin{cases}
1-\frac{e^{out_i}}{\sum_ke^{out_k}} && i=j
\\
- \frac{e^{out_j}}{\sum_ke^{out_k}}&& i \neq j
\end{cases}
$$
combined with the chain rule for vector functions
$$
\frac{\partial l}{\partial out_j}=\sum_k \frac{\partial l}{\partial \log p_k}\frac{\partial \log p_k}{\partial out_j}=\frac{\partial l}{\partial \log p_y}\frac{\partial \log p_y}{\partial out_j}=
\begin{cases}
\frac{e^{out_i}}{\sum_ke^{out_k}}-1 && y=j
\\
 \frac{e^{out_j}}{\sum_ke^{out_k}} && y \neq j
\end{cases}
$$
which we can write in vector notation as
$$
\frac{\partial l}{\partial out}=\exp(out)/\exp(out).\text{sum}() -\mathbb 1_{y}
$$
or just notice that the left side is just the logits so it's really $\log p - \mathbb 1_y$
#### Linear layer
The linear layer formula is $out=in\cdot W^T+b$ . Continuing with the chain rule we have
$$\frac{\partial l}{\partial W_{ij}}=\sum_{k}\frac{\partial l}{\partial out_{k}}\frac{\partial out_{k}}{\partial W_{ij}}$$
The k'th element of $out$ is the scalar product of $in$ with the k'th column of $W^T$ or the k'th row of $W$, ie
$$out_k=b_k+\sum_j in_j\cdot W_{kj}$$
the derivative of one output element with respect to a weight matrix element is then
$$
\frac{\partial out_{k}}{\partial W_{ij}}=
\begin{cases}
in_j && i=k\\
0 && else
\end{cases}
$$
and the derivative of the loss with respect to the matrix element is
$$\frac{\partial l}{\partial W_{ij}}=\frac{\partial l}{\partial out_{i}}\frac{\partial out_{i}}{\partial W_{ij}}=\frac{\partial l}{\partial out_{i}}in_j$$
Which we can write as the outer product of the two vectors
$$
\frac{\partial l}{\partial W}=\frac{\partial l}{\partial out}\otimes in
$$
the bias is simpler, we just have
$$\frac{\partial l}{\partial b_i}=\sum_{k}\frac{\partial l}{\partial out_{k}}\frac{\partial out_{k}}{\partial b_i}=\frac{\partial l}{\partial out_{i}}\frac{\partial out_{i}}{\partial b_i}=\frac{\partial l}{\partial out_{i}}\cdot 1$$
so it's just `dout`. Finally, for $in$,
$$
\frac{\partial out_{k}}{\partial in_{i}}=
W_{ki}
$$
$$\frac{\partial l}{\partial in_i}=\sum_{k}\frac{\partial l}{\partial out_{k}}\frac{\partial out_{k}}{\partial in_i}=\sum_k\frac{\partial l}{\partial out_{i}}W_{ki}=\frac{\partial l}{\partial out_{i}}W$$

#### ReLU
ReLU is quite easy, and since it's an element wise op we can skip all the sums. Let's say $\tilde{h}$ is the hidden activation before ReLU, ie $h_{i}=\max(\tilde h_i, 0)$. What's the derivative?
$$
\frac{\partial h_i}{\partial \tilde h_i}=
\begin{cases}
1 && \tilde h_i > 0
\\
0 && \tilde h_i < 0
\end{cases}
$$
the derivative doesn't exist at 0, but we don't care about that.
$$
\frac{\partial l}{\partial \tilde h_i}=\frac{\partial l}{\partial  h_i}\frac{\partial h_i}{\partial \tilde h_i}=
\begin{cases}
\frac{\partial l}{\partial  h_i} && \tilde h_i > 0
\\
0 && \tilde h_i < 0
\end{cases}
$$
#### Batches
One last detail regarding batches. The loss for a batch is the mean of the separate losses, so to backpropagate over the batch we just take the mean of the gradients for the different samples. I have a feeling that this is wasteful though, and maybe we can do better?

#### In code
The whole process looks like
```python
def backward(W1, b1, W2, b2, h, logits, y):
  dout = np.exp(logits)
  dout[range(logits.shape[0]), y] -= 1
  
  dh, dW2, db2 = dlin(dout, h, W2, b2)
  dh_hat = dh.copy()
  dh_hat[h == 0] = 0
  
  _, dW1, db1 = dlin(dh_hat, x, W1, b1)
  return dW1.mean(0), db1.mean(0), dW2.mean(0), db2.mean(0)
```
### Optimizing

We can also write an optimization loop
```python
epochs = 10
bs = 50
lr = 1e-1
for e in range(epochs):
  for i in range(0, len(x_train), bs):
    s = slice(i, min(len(x_train), i+bs))
    x = x_train[s]
    y = y_train[s]
    h, logits, loss = forward(x, y, W1, b1, W2, b2)
    dW1, db1, dW2, db2 = backward(W1, b1, W2, b2, h, logits, y)
    W1, b1, W2, b2 = map(lambda x: x[0]-lr*x[1], [(W1, dW1), (b1, db1), (W2, dW2), (b2, db2)])
  print(f"loss={loss}")
  print(f"acc={acc(logits, y)}")
```
which gets us such and such results
```
loss=0.6875153176459544
acc=0.76
loss=0.5454049286257023
acc=0.76
loss=0.4964384126281533
acc=0.78
loss=0.45487948890913216
acc=0.82
```

Tomorrow we'll work on the PyTorch abstractions.