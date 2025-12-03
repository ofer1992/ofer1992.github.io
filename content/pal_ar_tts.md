Title: Finding a Palestinian Arabic TTS model
Date: 2025-10-23 16:26
Category: Programming
Status: draft

I've been learning Palestinian Arabic for the last half a year or so. One of the challenges in Arabic is the fact that it is really a collection of dialects along with a literary language which serves as the respectable communication vehicle. This means less that a dialect like Palestinian Arabic has little learning material, written resources, few audiobooks compared to other languages like Spanish or German.

In language learning, I'm somewhat of a proponent of the Comprehensible Input approach, which dictates that to learn a language you should be passively (as in not being quizzed on the material) exposed to as much input as possible (audio, text) which is comprehensible (around 70% understanding) and interesting. When I learned German, I listened to audiobooks of The Little Prince, Percy Jackson, Harry Potter, The Hobbit and Lord of the Rings, which opened my eyes to the effectiveness of this method. Especially the audio format I found effective for me. But for Palestinian Arabic these things didn't exist. Well, with today's AI revolution, could we create this for ourselves?

In this post I'll will explore the TTS side of things for a couple of reasons:

- It is a bit easier to judge in terms of quality, even for a non-native speaker.
- Unlike text generation, the world of TTS model is a not as user-friendly and advanced. I could easily translate a chapter of Harry Potter using a model like Gemini 2.5 Pro for free, but to turn it into a good audio chapter is not as clear cut.
- TTS models are smaller, I can actually play around with them locally or on a cheap instance and finetune them myself.


## Commercial APIs

Let's see what we can get with the commercial offerings. Here's the sample sentence

**Arabic:**  
"امبارح رحت على سوق القدس القديمة واشتريت كعك بسمسم."

**Transliteration:**  
"Imbareh ruht 'ala suq il-Quds il-qadimeh w-ishtarait ka'ak b-simsim."

**English Translation:**  
"Yesterday I went to the market in the Old City of Jerusalem and bought sesame bread."

### ElevenLabs
ElevenLabs are pretty well known, not sure if because of marketing or actual quality. Anyway, they don't see to offer specific dialects within Arabic, but maybe the model is strong enough to recognize from the text that it's palestinian. They also have bracket syntax for narration instructions that might be used for instructing the dialect. Here's the sample I generated from their playground without much fiddling

![[el_yesterday_sample.mp3.mp3]]

This seems quite good. The drawbacks of Elevenlabs though are:

- It costs money. This isn't a big deal, though.
- They have a weird tier system limiting the amount of audio you can generate until you spend enough money - anti consumer (maybe they're afraid of data mining?).
- We don't get to play around with local models.