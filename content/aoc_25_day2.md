Title: Advent of Code 2025
Date: 2025-12-02 16:38
Category: Programming
Status: draft

AoC is back for another year! This time it's a bit shorter, only 12 days. Overall might be a good change, since in 2023 I fizzled out around day 20.

The first day has us simulating a dial ranging from 0 to 99 on a safe, where we needed to repeat a list of rotation instructions (left/right + number of clicks) and count how many times the dial ended up on 0. The second part complicated this by requiring to include the number of times the dial crossed 0, including during a rotation (so a rotation of 200 clicks clockwise would cross 0 point twice). This problems requires fairly straightforward modular arithmetic games, and I solved it successfully in python using a jupyter notebook.

I decided to solve today's problem using typescript. I programmed a lot in it in the last year on the job and I actually kind of like the language, but because we were very AI development-driven I didn't get to actually write much code myself, instead mostly prompting and reading. This robbed me of the tip-of-the-fingertips automaticity I have in python. I don't know what the future entails for programming, but for now, creating a ts file and not even remembering the for-loop syntax feels a little impotent.

Here's what I did then: I opened Claude Code side-by-side and instructed it to be a tutor and not make any code changes. This allowed me to get relevant answers to tech questions (syntax etc) quickly while still writing stuff manually. I think I'll also add some flashcards for the syntax (though I'm still a little ambivalent about it, boring flashcards are a net negative).

Today's problem was to parse a list of number ranges (11-22,33-100 etc) and then look for "doubled" numbers in those ranges, ie numbers of the form 123123, 3333, 11. Alright, bruteforce and stringifying solved it well enough. In fact, most of the time was spent on learning how to do ts dev with `nvim` (I love new toys), how to read the exceptions, and looking up silly syntax stuff (how to do floor division, `Math.floor(a / b)`).

The second part complicated the problem by having us consider a more general case, any periodic number, like 111, 123123123, 1414 etc. I had a tingling sensation, and then it came to me: I actually solved something similar at work! we had a problem where we had Gemini do OCR to pdfs, and it would sometimes go bonkers and generate really long repeating strings. We wanted to detect that. This was almost the same problem, except in our case, it was harder, because we were looking for a periodic **substring**. So how did I solve it? I couldn't recall... and why was that? because it was vibecoded!!!

Yep, it came back to bite me. I even remember putting time to understand how it solved it, after all it was my responsibility, and I did understand it at the time. And still, a few months later, I couldn't recall how it worked. Maybe I shouldn't be too harsh with myself, after all, I did remember that I had this problem, and maybe it's a responsible decision not to spend a lot of time on a math/algo problem in my fullstack startup job which requires to move fast bla bla bla. Nevertheless, here we were.

Anyway, after reading the code I figured it was probably not the right approach, and set out to solve it myself. The naive solution came to mind immediately:
- iterate on all the numbers in the ranges
- for each number, iterate on all possible periods (`p` can be a period if it divides the number of digits)
- for each period, check that `n[i] == n[i+p]` for all appropriate `i`.

Depending on the size of the ranges this approach could be good enough. But was there something better? I always look for the math angle. I remembered some leetcode problem which sounded similar, where given two strings `s1` and `s2` you need to decide if they are both periodic with the same pattern. The solution is to concatenate them twice, `s1s2` and `s2s1` and check for equality, as this is equivalent. Still, in our case this didn't help.

Then I had a whole deep think about how we can represent  this numbers as a tuple (pattern, n_periods).

<iframe src="https://claude.ai/public/artifacts/f15a9bba-6ca0-4b89-b1a9-f3d771912ce1"/>

After wrapping everything up and deciding to write a blog post, I of course immediately said to myself "why didn't you write it on the go, this would have made it less of a hassle". The next option that came to mind was to write a literate jupyter notebook (i've been looking at [solveit](https://solve.it.com/) recently) but that's for python. Or is it? quick google AI search told me there's a *deno* kernel which I installed. That solves two problems, the aforementioned one and the embarrassing REPL of js/ts, with the caveat being, this doesn't reproduce the real ts dev cycle. Still, one thing at a time, get good at the language, then learn the tooling.