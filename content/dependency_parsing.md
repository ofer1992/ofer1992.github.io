Title: Dependency Parsing
Date: 2025-11-23 14:18
Category: Programming
Status: draft

I watched the [dependency parsing lecture](https://www.youtube.com/watch?v=KVKvde-_MYc) from Stanford's NLP course about a month ago. I kinda got it fuzzily back then, but I figured I could use a refresher. Instead of rewatching the lecture I want to experiment with an AI-driven active learning approach, so I hooked up the lecture notes, the lecture transcript and the assignment to the new Gemini 3 Pro and asked it to tutor me on the subject.

We start by talking about dependency parsing as an idea in a dialogue fashion. This does mean that I have to later verify what I learned is correct. Now, in what I know about grammar you have words and relations between them, for example a verb has an object, a subject etc. Dependency parsing define a tree where a word is a head and has dependencies, for example in the phrase "I ate fish", "fish" and "I" are dependents of "ate". Why is that? one heuristic is to use the removal test, does the sentence make sense if I remove the head? in this case, the results are

- I -> ate fish 
- ate -> I fish
- fish -> I ate
the second option differs the most from the sentence in this case which tells us "ate" is the head.

Now, if a sentence is a tree, then what is the root? the axiomatic definition is that there should be a main verb and that is the root.

Okay, I wrote this mostly for myself to solidify, let's move on to the algorithm. The algorithm for building a dependency tree that we learn on the lecture is transition parsing. It represents the tree building as a process done by a machine as follows:
- a stack initialized with \[ROOT\]
- the sentence buffer \[I, ate, fish\]
- dependency list []
- a set of actions:
	- SHIFT: push the first word in the buffer into the stack
	- LEFT-ARC: makes the top of the stack the owner of the word below, and pops the word below, eg LEFT-ARC on \[ROOT, I, ate\] would add (ate -> I) to the the dependency list and pop "I".
	- RIGHT-ARC: similarly, except the top of the stack depends on the word below.

This defines a tree since a word is removed once it has a parent, and we stop only when all words are removed. I asked gemini, is that process capable of building any arbitrary tree. The answer is no, it requires the tree to be "projective". What that means is if we draw the arcs we defined over the sentence, then no two arcs cross one another (like parentheses). Is this requirement realistic? supposedly in English it is a reasonable assumption. In more flexible languages like Czech, it isn't.

By the way, I know my treatment above made this seem an easy problem, but consider the following sentences:
- Moscow sent troops into Afghanistan 
- Leaving the store unattended, I went outside to watch the parade
- I am extremely short
- Would you like brown rice or garlic naan?
It definitely requires a degree of knowledge in grammar to answer these correctly and confidently. Luckily, the labelers already did that for us, and we only need to train a model.

Let's move on to the [exercise](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/assignments/a2.pdf).