Title: Weekly Digest #1
Date: 2023-03-02 00:00
Category: Life
Status: published

Seems like I am not getting enough inspiration to write a well-developed post about something, so I am trying something new, collecting "micro-posts" about stuff I have done or read during the week. 

## Physics
I have an ongoing quest to learn physics. As it always is when learning by oneself, with no necessity but the joy of learning, there are countless tradeoffs to make. Do you study seriously from a textbook or an online course, devoting the same effort as was done in college, or do you watch YouTube videos with pretty animations? These are the two extremes; the first is difficult, slow, somewhat boring, and only pays off if you stick to it in the long run. Also, the effort is probably not calibrated to the goal. The second option is not enough, and whatever understanding is acquired tends to evaporate within a few days.

As for me, I'm floating within the bounds of this spectrum, although I am usually biased away from working hard. I mostly read and ponder. I think writing can be a very strong way to learn, as it forces you to explain, thus consolidating your knowledge and producing a product of your efforts. This helps combat the aforementioned evaporation (or a feeling of evaporation).

A great source of learning is the [*Feynman Lectures on Physics*](https://www.feynmanlectures.caltech.edu/). These are the notes from a 3 years course Feynman gave covering modern physics from an undergrad perspective. Unlike many dry and technical textbooks, they are written in Feynman's conversational tone, full of intuition, interesting derivations, etc. Even though math-wise I'm overqualified for the material, I still find it challenging and refreshing. Firstly, it's math as done by physicists, and that takes some getting used to. For example, approximations like $\sin x=x$ are implicitly taken, or differentials are treated in a way you wouldn't see in a math class. Secondly, the logic followed is physical, not mathematical, which is even more interesting to see and understand. In the end, solving a physical problem entails translating it to equations of motion and then solving them, but the difference between getting unsolvable equations and finding a solvable form depends on your physical intuition about the problem.

So that's what I do: I open a lecture that seems interesting and go over it. Sometimes it's not so clear, and I go read other sources, or go back to earlier lectures. Sometimes it's easy, and sometimes it's just right. I hope to write some more about physical ideas in future posts, like rotation, waves, heat and temperature, and Lagrangian and Hamiltonian mechanics. Of course, I have to learn them first.




## ChatGPT's API is released

OpenAI just released API access to ChatGPT, and compared to the regular interface, it's blazing fast. The way it works is, you send a request with the message history and you receive a response. Each message in the history is assigned either to the "user" or to the "assistant", with an optional "system" message to define the assistant's behavior. This way you can use the API for both the chat experience and as a regular text completion language model. 

The pricing was also updated, with 0.002&dollar; per 1k tokens. In human terms, this is approximately 600,000 words costing 2&dollar;. However, there is a catch, at least when using it for conversation. Each additional message requires the conversation history, which counts toward the used tokens. Hence, the number of tokens required for a conversation is quadratic in its length. If each message and reply take ~60 tokens (the tokens account for both the user's message and the assistant's reply), then the tokens required for each message would grow as
$$60,120,180,\dots,60n\dots$$
and the total token usage grows as
$$60, 180, 360,\dots,60\frac{(n+1)n}{2},\dots$$
How bad is that? well, if the messages are short then it's not too bad, but if you want to discuss some text or iterate over code, then pretty quickly the tokens per message count will be in the thousands. Comparing this pricing model to ChatGPT Pro's 20&dollar; flat rate, the latter can buy around 10 million tokens. I would guess that's way more than what you need for personal use, even if you plan to use it heavily. So why did I call it a catch? I think there is something counterintuitive about having to "pay" for words you already said over and over, but it's not that bad.
Performance-wise, it does seem to be less guarded than the chat version, although it's still nice. And now it remains to be seen what cool uses people would find.

## Other stuff
I hope to write in future posts about [Replacing Guilt](https://replacingguilt.com/), some basic economics (reading *Naked Economics*) and of course more mathematics and other random stuff.