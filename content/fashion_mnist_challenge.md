Title: bla bla
Date: 2024-08-08 13:10
Category: Dailies
Status: draft

Jeremy posted [a challenge](https://forums.fast.ai/t/a-challenge-for-you-all/102656) in [lesson 18](https://course.fast.ai/Lessons/lesson18.html) to reach the highest accuracy on the Fashion-MNIST test set within 5/20/50 epochs. The top results are around 95%, and it was last updated a year ago. I doubt I'll reach that, but today we'll implement a model, train it on the dataset and start iterating. This time we'll use the abstractions built during the course so far, so we'll get to focus more on the iteration and experimentation part of development.

We start by importing everything. I found out that miniai has [a module](https://github.com/fastai/course22p2/blob/master/miniai/imports.py) that basically imports everything, sparing us from all the boilerplate, so we just do
```python
from miniai.imports import *
```
The way the library is set up though, it's hard to know what we have imported from miniai. This nifty snippet will print all the imported names
```python
for g, v in globals().items():
  mod = getattr(v, '__module__', '')
  if not g.startswith('_') and mod.startswith('miniai'):
    print(mod, g)
```
which prints
<pre style='font-size: 13px'>
miniai.datasets inplace
miniai.datasets collate_dict
miniai.datasets show_image
miniai.datasets subplots
miniai.datasets get_grid
miniai.datasets show_images
miniai.datasets DataLoaders
miniai.init conv
miniai.conv to_device
miniai.conv collate_device
miniai.learner CancelFitException
miniai.learner CancelBatchException
miniai.learner CancelEpochException
miniai.learner Callback
miniai.learner run_cbs
...
</pre>

Next, to load the dataset
```python
ds = load_dataset("zalando-datasets/fashion_mnist")
```
and create the dataloaders with collation. Took me a bit to figure out, but we use the following

```python
x, y = ds['train'].features

@inplace
def transformi(b): b[x] = [TF.to_tensor(o) for o in b[x]]

dsd = ds.with_transform(transformi)
dls = DataLoaders.from_dd(dsd, 16)
```
We need the transform to convert from PIL to tensor, and then we have these utility methods from earlier lectures.

Next up, let's build a model and train it. First we're gonna go with vanilla conv.
```python
model = nn.Sequential(
  conv(1, 4), # 14x14
  conv(4, 8), # 7x7
  conv(8,16), # 4x4
  conv(16,16), # 2x2
  # conv(16,10, act=False)
  nn.Conv2d(16, 10, stride=1, kernel_size=2, padding=0),
  nn.Flatten()
)
x, y =  next(iter(dls.train))
x.shape, model(x).shape
```
This is similar to what I did in [[cnn_autoencoders]]. I did change the last layer, since we have a 2x2 grid, a 3x3 with stride 2 and padding has some useless parameters. Don't think it makes a difference, since they are just ignored in forward and backward passes, but who knows. 

```python
from torcheval.metrics import MulticlassAccuracy

bs = 256
lr = 2e-1
dls = DataLoaders.from_dd(dsd, bs)
metrics = [MulticlassAccuracy()]
l = TrainLearner(model, dls, F.cross_entropy, lr, [DeviceCB(), ProgressCB(plot=True), MetricsCB(*metrics)])

l.fit(5)
```

We use the learner class, and pass some callbacks for moving stuff to GPU, tracking progress and metrics. Fitting for 5 epochs yields
<div style="display: flex; justify-content: center; width: 100%; margin: auto;">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>MulticlassAccuracy</th>
      <th>loss</th>
      <th>epoch</th>
      <th>train</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0.471</td>
      <td>1.419</td>
      <td>0</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.716</td>
      <td>0.715</td>
      <td>0</td>
      <td>eval</td>
    </tr>
    <tr>
      <td>0.771</td>
      <td>0.605</td>
      <td>1</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.747</td>
      <td>0.665</td>
      <td>1</td>
      <td>eval</td>
    </tr>
    <tr>
      <td>0.816</td>
      <td>0.497</td>
      <td>2</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.795</td>
      <td>0.539</td>
      <td>2</td>
      <td>eval</td>
    </tr>
    <tr>
      <td>0.837</td>
      <td>0.443</td>
      <td>3</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.836</td>
      <td>0.450</td>
      <td>3</td>
      <td>eval</td>
    </tr>
    <tr>
      <td>0.849</td>
      <td>0.413</td>
      <td>4</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.820</td>
      <td>0.529</td>
      <td>4</td>
      <td>eval</td>
    </tr>
  </tbody>
</table>
  <img src="{static}images/fashion_loss.png" style="width: 50%; height: 50%; margin: 5px;" />
</div>
<!--![[fashion_loss.png]]-->
It looks like something's going on during the first epoch. Let's take another look:
![[fashion_loss_1epoch.png]]

One batch is especially bad, around step 70, but otherwise it's going okay.

Let's see how high we can get the LR. In fact, let's use the LRFinderCB.
```python
l.fit(cbs=[LRFinderCB()])
```
which displays
![[fashion_lr_finder.png]]
it's a graph of the loss of a batch over different learning rates. Usually there should be a small dip, and that where we take our LR from, but it seems like the jumps are too big. So let's change the parameters. The main one we have is `gamma` which is the multiplicative factor. Another way to think of it is the step size in log-space, so for example if `gamma=10` then each iteration moves on step in the graph above.

<hr>

I played around and couldn't really get that dip. I'm think maybe the initialization of the network is bad, so switch to investigating that first.

We add the `ActivationStats` callback and get back
![[act_stats0.png]]

And I just realized that I forgot to normalize the input. Okay, so what do we normalize? obviously the batch dimension has to "mean'd" over, and that leaves us with a tensor of shape `(C, H, W)`. The question is whether to go further and take the operation over `H` and `W`. I think so. I think we kinda assume by using convolutions that pixels have the same prior distribution, or that we're invariant to actual pixel location in image, so it wouldn't make sense to normalize them with different numbers. Another reason is that dividing by one number amounts to equalizing brightness, while if we do it on a per pixel basis it distorts the image. I don't know if that's a good reason though.

We're gonna do that with a (surprise surprise) callback
```python
xb, yb = next(iter(DataLoaders.from_dd(dsd, 1024).train))
xmean, xstd = xb.mean(), xb.std()
def _norm(b): return (b[0] - xmean) / xstd, b[1]
BatchTransformCB(_norm)
```
We immediately see the effect in the loss over 1 epoch
![[fashion_loss_1epoch_input_norm.png]]

And the activation statistics
![[act_stats1.png]]

though they still move over time.

What's next:
- norm layers
- better layer init
- optimizers
- lr schedule

<hr>

Trying with BN
```python
get_model_bn = lambda: nn.Sequential(
  conv(1, 4, norm=nn.BatchNorm2d), # 14x14
  conv(4, 8, norm=nn.BatchNorm2d), # 7x7
  conv(8,16, norm=nn.BatchNorm2d), # 4x4
  conv(16,16, norm=nn.BatchNorm2d), # 2x2
  # conv(16,10, act=False),
  nn.Conv2d(16, 10, stride=1, kernel_size=2, padding=0),
  nn.Flatten()
)
```
we get 
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: left;">
      <th>MulticlassAccuracy</th>
      <th>loss</th>
      <th>epoch</th>
      <th>train</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0.795</td>
      <td>0.579</td>
      <td>0</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.784</td>
      <td>0.577</td>
      <td>0</td>
      <td>eval</td>
    </tr>
    <tr>
      <td>0.859</td>
      <td>0.387</td>
      <td>1</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.834</td>
      <td>0.467</td>
      <td>1</td>
      <td>eval</td>
    </tr>
    <tr>
      <td>0.869</td>
      <td>0.355</td>
      <td>2</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.844</td>
      <td>0.425</td>
      <td>2</td>
      <td>eval</td>
    </tr>
    <tr>
      <td>0.877</td>
      <td>0.334</td>
      <td>3</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.838</td>
      <td>0.449</td>
      <td>3</td>
      <td>eval</td>
    </tr>
    <tr>
      <td>0.882</td>
      <td>0.319</td>
      <td>4</td>
      <td>train</td>
    </tr>
    <tr>
      <td>0.849</td>
      <td>0.416</td>
      <td>4</td>
      <td>eval</td>
    </tr>
  </tbody>
</table>

so we're up by 0.2% in validation, but the training is considerably slower now.

<hr>

One thing we can try with regards to initialization is to use the LSUV init.