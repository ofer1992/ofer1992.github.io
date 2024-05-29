Title: Yet another retrospective
Date: 2024-05-21 21:24
Category: Programming
Status: published

I expect another couple of days before I can submit a pull request. Today after some horrendous debugging I finally got some tangible progress. status, log, add-all and commit all seem to be working, perhaps even init (but still inconclusive). Still need to add push and pull. Then I need to connect it to config and add the necessary callbacks. In the end the minimal set of changes I converged to are just android git support, and keeping it in the same UX as the already existing implementation.

## Reflection
So, where did I go wrong? why did it take so long?

### Whittling down to the minimal set of changes
When I first set to work I thought I would completely replace the existinggit dependency and provide a unified implementation for electron, web and android, but what I personally needed was git in the android app. Instead of focusing straightaway on the android env (capacitor) I spent tons of time trying to understand and work with the other two envs, which both here their own set of quirks.

Start with the minimal thing you need.

### Tightning the debug loop, streamlining dev experience
Debugging was excruciating, working with async code, having to constantly move around from the clojure repl to chrome console, with an eye on the android IDE and the the services running in the background. There's just so much irreducible, unabstractable complexity. I felt like I constantly had to juggle 3-5 things in my mind. Some of it is inescapable: clojurescript to javascript to android, there are just too many things going on. Still, I'm sure I made my life unnecessarily hard by not taking enough time to learn best practices. Good dev hygiene and have saved me a third of the time spent debugging.

### Specifying the adapter in advance
In retrospect the hardest part of the work was building the bloody file system adapter that you pass to the isogit functions. It has the same API like node's file system, but it only requires a few functions. I had some reference, and my approach was to build something quickly and just tinker with it until it works. That was a big mistake.

First of all it meant I had to debug a lot, especially interop code, and debug through isogit's code. There was also a particularly nasty fact that this library likes to silence exceptions (which now makes me think that I should have set the break on caught exception" more often).

What I should have done is carefully specify and write down the input output of the adapter by poking nodeFS. More work upfront but better down the line.

### Producing more content
There was plenty of opportunity to do some tutorials and technical writing about what I learned. It does slow down the progress, but it's worth it in the long run, for others and for myself.


Anyway, let's get to the PR milestone this week!