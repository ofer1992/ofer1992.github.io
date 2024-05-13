Title: More thoughts on logseq, git, and how to approach open source tasks
Date: 2024-05-13 18:00
Category: Programming
Status: published

## Where I am

It's been a couple more days now since my last post on the subject. I spent another 10 hours or so, and haven't gotten much further. Mostly I'm stuck with file system problems. In my last post I said I would use filesystem abstraction already present in the logseq code base. By now I feel that was a wrong decision. At first glance using the abstraction seems good, because it frees me of addressing the three environments available: electron, browser and android/ios. In reality though, reasons:
- some requirements are not supported: reading binary files isn't available without changing the underlying implementation of the browser `fs`.
- while the available `fs` interface seems similar to the one required by `isometric-git` there are differences which require writing an adapter. this on it's own is not too bad, but the more I worked on building one, the more I realised that this will be an arduous process of investigating each failure point, figuring out whether I can address it in the adapter or I need to change the backend.
- debugging is hard. the heavy usage of interop and promises makes it challenging to quickly debug things. some of it is probably on me, I'm not experienced in this dev environment.
- the interface doesn't seem to be defined strictly enough to guarantee expected behavior. therefore again, a lot of debugging for all environments
- the browser fs is especially limiting, more and more I need to get in there and change things
So, I'm not saying it's impossible, but it's a lot of work, and of course, changing such fundamental implementation as the file system is dangerous and error prone.

What's the alternative? isogit expects the file system to follow a certain API like node's. Electron is already using node `fs`, and capacitor is also quite similar. The browser isn't, but it's also not a top priority, I don't think most people actually use it.

I decided then to write the minimal adapters I need to work from each platform's file system. It's still a bit of work, since the adapter communicates with the electron process through a message passing system, which again hides node's `fs` behind a layer of abstraction. I wrote something quickly without testing, and I hope it will work without too much work. 

## Reflecting on my development process
I'm maybe 20 hours in already, and I feel somewhat frustrated. I guess I expected that by now I'll already have a working prototype, a nice pull request and a satisfied smug. Still, reality is better than fantasy, and I should probably learn something from this. 

### Familiarity with tools
A big time cost is my lack of familiarity with much of the stack. clojurescript, shadow-cljs, javascript, node, electron, js async programming, web APIs like File System API, debugging and good dev practices in this environment, that's at least on the top of my head. Each of those is a potential stumbling block in the next bug I run into.

On the other hand, my goal is not to master all of this subject but to implement something specific, so there's a tradeoff here of time invested in methodical learning vs time wasted from lack of familiarity.

### Strategic planning
It's the second time since I started that I change my plan of how to complete this task, and I ask myself whether it's something that could have been avoided. In fact, while talking with a friend about where I am with this project he specifically told me that I should not try to use logseq's `fs` abstraction but write everything myself, and I didn't accept it. I guess I wanted to uphold code reuse. 

I couldn't formulate a plan immediately, since I knew diddly squat about the code, so some time for exploration and familiarization with the code base is needed. Perhaps I could allocate some time specifically to explore the code, say 3-4 hours, play around and see how stuff work, and then formulate several alternative each with its pros and cons. It may have set me on the path I'm on faster.

### Get help
I still haven't given a shout out in discord. I'm sure having someone knowledgable helping me could have cut the time by a significant factor, but even now I'm reluctant. I wanted to wait until I have a prototype that works to start a pull request and talk about it. What's stopping me? I always liked working solo, for whatever reasons. I hope that with enough suffering I'll learn my lesson, humble myself and ask for assistance.

### Accepting reality
In the end, this things take time. I think it feels more painful when it's on my own free time. What do I care when it's a task for work? it takes what it takes, I get paid hourly, and no one can complain, it's hard. Now time spent on this project is time not spent on something else.

I don't want to give up. It's important for me to see this through at least to the point of a prototype and publishing. I also think this is important experience, but practically in how to approach and execute such projects, and psychologically, how to cope with what it brings, and what I can expect in future projects. Reality is better than fantasy.






