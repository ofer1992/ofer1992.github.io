Title: Switching Logseq's git dependency from dugite to isomorphic-git: The journey so far
Date: 2024-05-08 18:10
Category: Life
Status: draft

## The goal
A short recap of where we are (will probably refactor this to retroactive posts eventually): I'm trying to switch logseq's git dependency from `dugite` to `isomorphic-git`, so it can run on android, browser etc. The problem with dugite is that it depends on the presence of a git client. Since git in logseq is only expected to work on a pc or mac using electron, the implementation is tied to electron specific code like a separate config and state, and a different access to the file system. Also, dugite can run arbitrary git commands while iso-git has specific functions that implement most of the functionality of git, but obviously it is more restricted.

## Day 1 - Warming up with ClojureScript, interop with isomorphic-git
Since logseq is written in ClojureScript, the first step was setting up the dev environment. It is luckily relatively well-documented. Of course, in my opinion clojure's general dev environment is quite clunky. Maybe I'm spoiled, having come from python which is interpreted language, and with which I have much experience, but I never quite manage to wrap my head around all the scaffolding required for clojure development. You need java, and clojure, initialize the project in a certain way, and then you compile and run it (or run it with one of the clojure CLI commands). This is the barebones setup, but of course you want a repl, so you need some more tools. I use VSCode+Calva. And you also have build tools like leiningen or shadow-cljs, and then there's all the interop with java/javascript. Now, a lot of effort has went to make things work out-of-the-box, but still, there's a lot of complexity going on which in the end is still leaky. Sorry for the rant, but I had to get it off my chest.

After setting up and figuring out the program's endpoints and different execution modes (browser or electron, haven't touched mobile yet), I scanned the source code for usage of git. The first hurdle was to figure out the javascript interop. You can call javascript functions directly from clojurescript, which is super neat, but it takes some figuring out the right syntax. Here ChatGPT was a big help, basically helping me do it in minutes instead of an hour in the worst case. Another hurdle was promises. iso-git uses promises for all the operations, and for some reason things were not working as I expected. Prints weren't printing. Again, this is a classic example of the dillema of going deep on subjects or hacking along. I'm not very knowledgable of concurrent programming, and especially not in clojure, so it was very challenging for me to understand what's going on, or what sanity checks should I do. In the end I also figured out that the problem was really just printing: depending on the usage of `js/console.log` vs `println` or `prn` you get prints in either the browser console or the repl output or wherever. So that's was a lesson learned with sweat and tears. In fact, this whole process, as we will see, exemplifies the sweat and tears required to learn these lessons.

## Day 2 - Actually writing some code
I then moved on to rewriting the basic git functions in the code with isomorphic-git. Again, with the help of Copilot and ChatGPT, this process went fairly smoothly, and thanks to the repl, it's very quick to check that the functions behave as expected. By this point I got the electron version to work with the new implementations of the git functionality. Clearly all that remained was to reenable the git tab in the settings modal. A quick look through the code led me to the test that checks if electron is running and only then displaying the git setting, which gladly commented out. Immediately the tab appeared in the browser version.

I patted myself on the back for my success, but then quickly realized this was the easy part. Nothing was actually happening on the git side. You see, since using dugite already restricted the git integration to computers, the code naturally became tied to the electron build, so the git configuration and the callbacks that manage the git lifecycle didn't actually work. I had to refactor those dependencies out to the more general `frontend` build.

## Day 3 - Moving state from electron to frontend
Where was logseq's state located? and how? my investigation began by trying to trace a simple toggle button present in the editor tab of the settings page. After searching for the toggle's label in the codebase I found the following
```clojure
(defn outdenting-row [t logical-outdenting?]
  (toggle "preferred_outdenting"
          [(t :settings-page/preferred-outdenting)
           (ui/tippy {:html        (outdenting-hint)
                      :class       "tippy-hover ml-2"
                      :interactive true
                      :disabled    false}
                     (svg/info))]
          logical-outdenting?
          config-handler/toggle-logical-outdenting!))
```
There was a getter called `logical-outdenting?` and a setter called `toggle-logical-outdenting!`. They were both under the `frontend` namespace, but in different files, `state.cljs` and `config.cljs`. The getter referred to an atom called state, but it must have been loaded from somewhere on disk, since the info was persisted. The setter changed the values on a file called `config.edn`. This is actually just the config file which is even accessible from logseq itself.

I was a bit puzzled about how the config file and the state atom are maintained in sync, but I decided to just hope it works. Initially after adding new getters and setters for the git configuration, I thought it wasn't working, but playing around a bit I noticed that the config.edn file was indeed updated.

From there on it was fairly straightforward work of replacing all the references to the usage of electron state to the new properties I defined. I even did some ui coding refactoring with the help of ChatGPT. It definitely seems like the git integration was written in an earlier part of development, since it's somewhat inconsistent in style from the rest of the code.
## Day 4 - How do I even access the file system
Today was mostly spent puzzling over the file system access and how it works in the browser. Again, an example of implementation details, the understanding of which is earned through sweat and tears. Or asking around on Discord, which is something I'm not good at and should probably do more often. 

Since logseq runs on several platform, there is an abstraction implemented in `fs.cljs` that create a unified interface. It is implemented through the use of protocols, which is a clojure construct that implements polymorphism, and one I have not used before. The combination of protocol, browser filesystem access, promises and maybe more really slowed me down today. I would say it was around 3 hours just to figure out how access to the fs works, what I can expect to be able to do, why did some files not appear initialliy (they were filtered), why were some calls not working (promises are so obtuse, but I probably could have used `.catch`). I think I understand enough to try and use iso-git with this abstraction, but there are still some question marks remaining.

There is also one weird thing I need to make a decision about: the old git implementation maintains the gitdir (`.git`) not in the actual repo but on logseq's appdata folder. Can I handle that? what about access permissions? all will be seen tomorrow.

## Looking ahead
