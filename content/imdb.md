Title: IMDB Reviews sentiment analysis
Date: 2024-07-02 14:17
Category: Programming
Status: draft

>"It’s better to do something simple which is real. It’s something you can build on because you know what you’re doing. Whereas, if you try to approximate something very advanced and you don’t know what you’re doing, you can’t build on it." - Bill Evans

Recently I've been trying to brush up on my deep learning practitioner skills, which have atrophied over the last year or so of disuse. Well, not just brush up, but deepen, expand enrich, as what I did in my Masters was really just a part of the work required. I kept trying to approach exciting and ambitious projects only to end up feeling paralysed and overwhelmed, and giving up on them. Luckily I did some honest thinking and acknowledged that my grasp of the practical basics was not strong enough, which meant going back to the woodshed. Also, small projects can act as small wins and box ticks, creating momentum etc.

Today were tackling the *IMDB movie sentiment classification* database. It contains 50k examples of a binary classification task, deciding whether a movie review is positive or negative. I got the idea from the Claude chatbot, and we will follow Claude's "six-steps plan", each step in its own section.
## "Understand the problem and the dataset"
The first step is to download the data from [here](https://ai.stanford.edu/~amaas/data/sentiment/). Since we're cool, we're gonna use `curl` and `tar`. Looking at the extracted folder we see the following structure (reduced to the relevant files)
```
aclImdb
├── README
├── test
│   ├── neg
│   │   ├── {id}_{rating}.txt
│   │   ├── ...
│   ├── pos
│   │   ├── {id}_{rating}.txt
│   │   └── ...
└── train
    ├── labeledBow.feat
    ├── neg
    │   ├── {id}_{rating}.txt
    │   ├── ...
    └── pos
        ├── {id}_{rating}.txt
        ├── ...
```
Each text file is a review. The folder determines the label, and we already have a test-train split. Let's look at a review:
```
cat aclImdb/train/pos/2435_8.txt 

I never thought an old cartoon would bring tears to my eyes! When I first purchased Casper & Friends: Spooking About Africa, I so much wanted to see the very first Casper cartoon entitled The Friendly Ghost (1945), But when I saw the next cartoon, There's Good Boos To-Night (1948), It made me break down! I couldn't believe how sad and tragic it was after seeing Casper's fox get killed! I never saw anything like that in the other Casper cartoons! This is the saddest one of all! It was so depressing, I just couldn't watch it again. It's just like seeing Lassie die at the end of a movie. I know it's a classic,But it's too much for us old cartoon fans to handle like me! If I wanted to watch something old and classic, I rather watch something happy and funny! But when I think about this Casper cartoon, I think about my cats!
```

Wow, almost looks fake. Here's the same id but from the negative folder
```
cat aclImdb/train/neg/2435_1.txt 

I will warn you here: I chose to believe those reviewers who said that this wasn't an action film in the usual sense, rather a psychological drama so you should appreciate it on that basis and you will be alright.<br /><br />I am here to tell you that they were wrong. Completely wrong.<br /><br />Well, no, not completely; it is very disappointing if you are looking for an action flick, they were right about that. But it is also very unsatisfying on all other levels as well.<br /><br />Tom Beringer wasn't too bad, I suppose, no worse than usual; but what possessed them to cast Billy Zane in this? Was it some sort of death wish on the part of the producers? A way to made their film a guaranteed flop? In that case, it worked.<br /><br />If they were actually aiming for success, then why not cast somebody who can act? Oh, and might as well go for a screenwriter who knows how to write. Ah, yes, and a director who knows how to direct.<br /><br />As someone who sat through this mess, actually believing it would shortly redeem itself, I can assure you it never did. Pity, it could've been a good film.
```
Here we also see some html tags, which we will probably want to filter out. That's a classic example of why it's good to look at the data, since some unexpected thing can always mess with your model.
## "Preprocess the data"
Since the dataset is relatively small (couple hundred mb), we can afford to load it in memory. 
```python
import os
from pathlib import Path

data = {}
for split in ['train', 'test']:
    data[split] = {}
    for label in ['pos', 'neg']:
        data[split][label] = []
        p = Path(f'aclImdb/{split}/{label}')
        for name in os.listdir(dir):
            with open(dir/name) as f:
                data[split][label].append(f.read())
```
This snippet will load all the data into a dictionary mirroring the folder structure.

Even though we're still in the preprocessing stage, we already need to start considering our model, because this determines the kind of preprocessing we do. We will take as a baseline a combination of bag-of-words and logistic regression. bag-of-words will produce a vector which we can feed into the logistic regression. Bag-of-words turns a sentence into a vector by counting the number of occurrences of each word, (like the `Counter` data structure in python's `collections`, but as a vector). Since we turn it to a vector, we must select some size for the vocabulary, the set of words the model recognizes. We'll consider words to be a space delimited string, and get rid of punctuation. The size of the vocabulary will be determined from the distribution of words in the corpus, or to put it differently, we're going to try to choose a number that's small while still not requiring us to throw away a lot of words.

We also do some preprocessing by turning everything to lower-case and getting rid of punctuations.
```python
import re
from collections import Counter

c = Counter()
for r in data['train']['pos']+data['train']['neg']:
    c.update(re.sub(r'[^a-z\s]', '', r.lower()).split())
```

The top 10 words in the corpus are then
```
Counter({'the': 334760,
         'and': 162243,
         'a': 161962,
         'of': 145332,
         'to': 135047,
         'is': 106859,
         'in': 93038,
         'it': 77110,
         'i': 75738,
		 ...
```
Of course, all the most common words are quite generic. We can plot the this on a graph.
<p style="width:50%; margin:auto">
  <img src="{static}images/plot_words.png" />
</p>
<!--     ![[plot_words.png]] -->
Some thoughts before we move on:
- The most common words are actually not useful at all on their own.
- We see from the graph that about half the words appear only once.
- Since the number of words we take determines the dimensions of the feature vector, we should keep in mind the number of training samples we have (~50k). We want the number of features to be small enough to avoid overfitting.
- We can surely reduce the number of words by using better tokenization. For example, in our current scheme a word like "valentine's" turns to "valentines", but the interesting word is really "valentine".

For now, we start with an arbitrary vocab_size of 5000.
```python
vocab_size = 5000
vocab = {k: i for i, k in enumerate(sorted(c, key=c.get, reverse=True)[:vocab_size])}
```

And we use it to build a feature vector by counting occurrences of words that are in the vocabulary.
```python
def features(review, vocab):
    words = tokenize(review)
    vec = np.zeros(len(vocab))
    for w in words:
        if w in vocab:
            vec[vocab[w]] += 1
    return vec

features("the bear was awesome", vocab)
# array([1., 0., 0., ..., 0., 0., 0.])
```

The final thing before we move on is to extract out from the train dataset a validation set, which we can use to tune hyperparameters and compare models, while saving the test set for the final evaluation.

```python
import random
seed = 42
N = len(data["train"]["pos"])
val_size = N // 10
rnd = random.Random(42)
val_idxs = sorted(rnd.sample(range(N), val_size))
train_idxs = list(set(range(N)) - set(val_idxs))

def get_subset(ds, idxs, vocab):
    X = []
    y = []
    for ind in idxs:
        X.append(features(ds["pos"][ind], vocab))
        y.append(0)
        X.append(features(ds["neg"][ind], vocab))
        y.append(1)
    return np.array(X), np.array(y)

X_train, y_train = get_subset(data["train"], train_idxs, vocab)
X_val, y_val = get_subset(data["train"], val_idxs, vocab)
```
## "Build a simple baseline model"
The only thing left now is to train a logistic regression model. We'll use sklearn (perhaps in a future project I'll do a pure numpy approach). Using sklearn is quite straightforward

```python
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(penalty=None)
logreg.fit(X_train, y_train)

print(f'train acc={np.mean(logreg.predict(X_train) == y_train)}')
print(f'val acc={np.mean(logreg.predict(X_val) == y_val)}')

# train acc=0.9420888888888889
# val acc=0.8636
```

Out of the box we get a 85% on the validation set. We also see we are overfitted. In fact, if we increase the max_iter parameter to 2000 we get up to
```
train acc=1.0
val acc=0.8252
```
A perfect fit on the training set, while the validation set takes a hit. It's a good test to see if we can perfectly fit on the train set. It's not always possible, as it depends on the capacity of the model. In our case, since the model has 5k features to choose from, the training set has ~20k samples and regularization is disabled, it isn't surprising. In fact, the default value of max_iter=100 serves as early stopping which is a kind of regularization!

A nice thing about logistic regressions is interpretability: we can deduce which words are informative to the label and which aren't. For example, here are the 10 words with the lowest weights: *attached*, *fooled*, *irish*, *reference*, *repeatedly*, *editor*, *between*, *literally*, *ive*, *according*. And here's the 10 words with most weights: *waste*, *poorly*, *disappointment*, *lacks*, *worst*, *mess*, *awful*, *pointless*, *worse*. Surprisingly, they're all negative.

Another cool thing we can do is color an example by the weights of each word, for example

> '<span style="background-color: rgb(0,255,0, 0.04265246106422292)">i </span><span style="background-color: rgb(255,0,0, 0.47033456488848235)">am </span><span style="background-color: rgb(255,0,0, 0.4123712301321726)">writing </span><span style="background-color: rgb(0,255,0, 0.005917706458466877)">this </span><span style="background-color: rgb(0,255,0, 0.1711111210441242)">after </span><span style="background-color: rgb(255,0,0, 0.20433823707379858)">just </span><span style="background-color: rgb(0,255,0, 0.037058791671422064)">seeing </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(0,255,0, 1.0)">perfect </span><span style="background-color: rgb(0,255,0, 0.010033675210943335)">son </span><span style="background-color: rgb(255,0,0, 0.00889010358876386)">at </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(255,0,0, 0.23447409537885475)">gay </span><span style="background-color: rgb(0,255,0, 0.04049596375782109)">and </span><span style="background-color: rgb(255,0,0, 0.13748898030755594)">lesbian </span><span style="background-color: rgb(255,0,0, 0.0)">mardi </span><span style="background-color: rgb(255,0,0, 0.0)">gras </span><span style="background-color: rgb(0,255,0, 0.04199020472459187)">film </span><span style="background-color: rgb(255,0,0, 0.08689733441221965)">festival </span><span style="background-color: rgb(255,0,0, 0.023830296022082025)">in </span><span style="background-color: rgb(255,0,0, 0.0)">sydney </span><span style="background-color: rgb(255,0,0, 0.0)">australiabr </span><span style="background-color: rgb(255,0,0, 0.046000518108140584)">br </span><span style="background-color: rgb(0,255,0, 0.01726310627565952)">when </span><span style="background-color: rgb(0,255,0, 0.04531886820138982)">their </span><span style="background-color: rgb(0,255,0, 0.05007746999638212)">father </span><span style="background-color: rgb(0,255,0, 0.062016106149632086)">dies </span><span style="background-color: rgb(0,255,0, 0.07709865986070619)">two </span><span style="background-color: rgb(255,0,0, 0.0)">estranged </span><span style="background-color: rgb(0,255,0, 0.5727940740901919)">brothers </span><span style="background-color: rgb(0,255,0, 0.01985040840007181)">meet </span><span style="background-color: rgb(255,0,0, 0.00889010358876386)">at </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(255,0,0, 0.010560443738167133)">funeral </span><span style="background-color: rgb(0,255,0, 0.04049596375782109)">and </span><span style="background-color: rgb(0,255,0, 0.1711111210441242)">after </span><span style="background-color: rgb(255,0,0, 0.0)">discovering </span><span style="background-color: rgb(0,255,0, 0.02277322625694133)">that </span><span style="background-color: rgb(0,255,0, 0.005853600023155638)">one </span><span style="background-color: rgb(255,0,0, 0.0546631791445451)">of </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(0,255,0, 0.5727940740901919)">brothers </span><span style="background-color: rgb(0,255,0, 0.03975000481815559)">is </span><span style="background-color: rgb(255,0,0, 0.46594456982156596)">dying </span><span style="background-color: rgb(0,255,0, 0.03050817801804005)">from </span><span style="background-color: rgb(0,255,0, 0.5274303823274182)">aids </span><span style="background-color: rgb(0,255,0, 0.0006889932301914058)">they </span><span style="background-color: rgb(255,0,0, 0.2178510621956707)">enter </span><span style="background-color: rgb(255,0,0, 0.026551338327775703)">on </span><span style="background-color: rgb(0,255,0, 0.018766106797469113)">a </span><span style="background-color: rgb(0,255,0, 0.29575443223014675)">heart </span><span style="background-color: rgb(255,0,0, 0.0)">warming </span><span style="background-color: rgb(0,255,0, 0.2789858210725884)">journey </span><span style="background-color: rgb(255,0,0, 0.0546631791445451)">of </span><span style="background-color: rgb(255,0,0, 0.0)">reconciliation </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(0,255,0, 0.07709865986070619)">two </span><span style="background-color: rgb(255,0,0, 0.1752621503741513)">leads </span><span style="background-color: rgb(255,0,0, 0.057936981045791466)">do </span><span style="background-color: rgb(0,255,0, 0.018766106797469113)">a </span><span style="background-color: rgb(0,255,0, 0.31894725396446727)">magnificent </span><span style="background-color: rgb(0,255,0, 0.43603428597777316)">job </span><span style="background-color: rgb(255,0,0, 0.0546631791445451)">of </span><span style="background-color: rgb(0,255,0, 0.34370407142168613)">creating </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(255,0,0, 0.0)">gradual </span><span style="background-color: rgb(0,255,0, 0.13801630244060087)">warmth </span><span style="background-color: rgb(0,255,0, 0.04049596375782109)">and </span><span style="background-color: rgb(0,255,0, 0.08307937127739665)">respect </span><span style="background-color: rgb(0,255,0, 0.02277322625694133)">that </span><span style="background-color: rgb(0,255,0, 0.41264595325176184)">builds </span><span style="background-color: rgb(255,0,0, 0.0037656056507315884)">up </span><span style="background-color: rgb(255,0,0, 0.0005082240436384793)">between </span><span style="background-color: rgb(0,255,0, 0.02155107873516601)">them </span><span style="background-color: rgb(0,255,0, 0.03293032022576033)">as </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(255,0,0, 0.0010141747206862505)">movie </span><span style="background-color: rgb(255,0,0, 0.2515080627646316)">progresses </span><span style="background-color: rgb(0,255,0, 0.04265246106422292)">i </span><span style="background-color: rgb(255,0,0, 0.057936981045791466)">do </span><span style="background-color: rgb(255,0,0, 0.005389831551733009)">have </span><span style="background-color: rgb(0,255,0, 0.005853600023155638)">one </span><span style="background-color: rgb(255,0,0, 0.0)">qualm </span><span style="background-color: rgb(0,255,0, 0.005558015722499624)">about </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(255,0,0, 0.0010141747206862505)">movie </span><span style="background-color: rgb(0,255,0, 0.18200352019602964)">though </span><span style="background-color: rgb(0,255,0, 0.5091752338602896)">whilst </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(255,0,0, 0.14565127351756196)">brother </span><span style="background-color: rgb(0,255,0, 0.10452514896375287)">who </span><span style="background-color: rgb(0,255,0, 0.03975000481815559)">is </span><span style="background-color: rgb(255,0,0, 0.46594456982156596)">dying </span><span style="background-color: rgb(255,0,0, 0.35483749359155314)">acts </span><span style="background-color: rgb(0,255,0, 0.07185952950061382)">sick </span><span style="background-color: rgb(0,255,0, 0.008901308124265633)">he </span><span style="background-color: rgb(255,0,0, 0.12364899546684406)">doesnt </span><span style="background-color: rgb(255,0,0, 0.29274542256906116)">look </span><span style="background-color: rgb(0,255,0, 0.09865015779476502)">it </span><span style="background-color: rgb(0,255,0, 0.018766106797469113)">a </span><span style="background-color: rgb(255,0,0, 0.1668493690989387)">person </span><span style="background-color: rgb(255,0,0, 0.0546631791445451)">of </span><span style="background-color: rgb(255,0,0, 0.1340400358458006)">t </span><span style="background-color: rgb(255,0,0, 0.0)">cells </span><span style="background-color: rgb(255,0,0, 0.22614030218687553)">would </span><span style="background-color: rgb(255,0,0, 0.29274542256906116)">look </span><span style="background-color: rgb(0,255,0, 0.16607486475348793)">quite </span><span style="background-color: rgb(255,0,0, 0.1927342060191777)">ill </span><span style="background-color: rgb(255,0,0, 0.2135627740706253)">not </span><span style="background-color: rgb(255,0,0, 0.21862099168415838)">even </span><span style="background-color: rgb(0,255,0, 0.018766106797469113)">a </span><span style="background-color: rgb(255,0,0, 0.16287371743106116)">make </span><span style="background-color: rgb(255,0,0, 0.0037656056507315884)">up </span><span style="background-color: rgb(0,255,0, 0.43603428597777316)">job </span><span style="background-color: rgb(0,255,0, 0.004166560555322963)">to </span><span style="background-color: rgb(255,0,0, 0.16287371743106116)">make </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(255,0,0, 0.007313930534815736)">actor </span><span style="background-color: rgb(255,0,0, 0.29274542256906116)">look </span><span style="background-color: rgb(255,0,0, 0.1927342060191777)">ill </span><span style="background-color: rgb(255,0,0, 0.0145737819082238)">was </span><span style="background-color: rgb(255,0,0, 0.0)">employed </span><span style="background-color: rgb(0,255,0, 0.018766106797469113)">a </span><span style="background-color: rgb(0,255,0, 0.158058472476663)">small </span><span style="background-color: rgb(255,0,0, 0.0)">gripe </span><span style="background-color: rgb(255,0,0, 0.08469344942881546)">but </span><span style="background-color: rgb(0,255,0, 0.005853600023155638)">one </span><span style="background-color: rgb(0,255,0, 0.02277322625694133)">that </span><span style="background-color: rgb(0,255,0, 0.32187586838630966)">makes </span><span style="background-color: rgb(0,255,0, 0.09865015779476502)">it </span><span style="background-color: rgb(0,255,0, 0.018766106797469113)">a </span><span style="background-color: rgb(0,255,0, 0.5598511367945777)">bit </span><span style="background-color: rgb(255,0,0, 0.30057838928476655)">less </span><span style="background-color: rgb(0,255,0, 0.6973250944274204)">realistic </span><span style="background-color: rgb(255,0,0, 0.21561431687360214)">despite </span><span style="background-color: rgb(0,255,0, 0.02277322625694133)">that </span><span style="background-color: rgb(0,255,0, 0.005853600023155638)">one </span><span style="background-color: rgb(0,255,0, 0.158058472476663)">small </span><span style="background-color: rgb(255,0,0, 0.0)">gripe </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(0,255,0, 1.0)">perfect </span><span style="background-color: rgb(0,255,0, 0.010033675210943335)">son </span><span style="background-color: rgb(0,255,0, 0.03975000481815559)">is </span><span style="background-color: rgb(0,255,0, 0.018766106797469113)">a </span><span style="background-color: rgb(0,255,0, 0.8463934170414216)">wonderful </span><span style="background-color: rgb(255,0,0, 0.0010141747206862505)">movie </span><span style="background-color: rgb(0,255,0, 0.04049596375782109)">and </span><span style="background-color: rgb(255,0,0, 0.09809706471839275)">should </span><span style="background-color: rgb(0,255,0, 0.1726900761126281)">you </span><span style="background-color: rgb(255,0,0, 0.005389831551733009)">have </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(0,255,0, 0.267467502899476)">chance </span><span style="background-color: rgb(0,255,0, 0.004166560555322963)">to </span><span style="background-color: rgb(0,255,0, 0.1194936305501035)">see </span><span style="background-color: rgb(0,255,0, 0.09865015779476502)">it </span><span style="background-color: rgb(255,0,0, 0.057936981045791466)">do </span><span style="background-color: rgb(255,0,0, 0.15038044247997384)">im </span><span style="background-color: rgb(255,0,0, 0.9599913784742594)">hoping </span><span style="background-color: rgb(0,255,0, 0.018827632956966555)">for </span><span style="background-color: rgb(0,255,0, 0.018766106797469113)">a </span><span style="background-color: rgb(0,255,0, 0.006677882670571365)">dvd </span><span style="background-color: rgb(0,255,0, 0.7987768631803601)">release </span><span style="background-color: rgb(255,0,0, 0.023830296022082025)">in </span><span style="background-color: rgb(0,255,0, 0.041456744665536324)">the </span><span style="background-color: rgb(255,0,0, 0.14687484867974562)">near </span><span style="background-color: rgb(0,255,0, 0.3396042283541725)">future </span>'

Since the final classification is the sum of `weight*n_occurences` it illustrates clearly what in the sentence affects the classification. It also illustrates the problem with classifying based on words, even in the simple example of negation "not wonderful" and "wonderful" will still have the same contribution from wonderful.

Anyway, we have a baseline. In the next section we face the realm of infinite possibilities of tweaking.
## Iterate and improve the model
We will continue the good work in the next post, but I'll just sketch the next things we can look at.
### Figuring out where the model is wrong
If we want to improve the model, we have to figure out what it got wrong and why. This involves looking at misclassified examples, and coming up with ideas for improvements.
### Improvements
There are many things we can try, and when we if we consider combinations, stuff become exponential. Let's list a few things we could consider:
#### Tokenization
This is one thing we could work on that would give us an improvement across the board, as our current scheme is amount to converting to lower case and removing anything that isn't a letter.  We could improve the clean-up and get rid of some `<br>` tags. We can try to apply more NLP pre-tokenization techniques that standardize the data even more. We can use a data-oriented tokenizer like BPE. We can experiment with different vocabulary sizes.
#### Feature vector
Right now we are using a simple word count. There are other available techniques, culminating in deep learning models that produce semantic embeddings as vectors. 
#### Different models
Finally, we could try a different type of model, such as Naive Bayes, or a RNN/transformer.
