Title: The mysteries of HTML box heights
Date: 2024-04-02 18:30
Category: TILs
Status: published

Today's post is not "fully cooked", I still don't think I figured this topic out, but I did learn a few things.

Today I needed to do some css hacking for a dashboard I'm building with `streamlit`. I was using a `grid` element from the streamlit-extras package, and I wanted to create a card component with a title and description by injection html into the app. I couldn't get the card to fill its square in the grid. Setting `height: 100%;` didn't help. From looking at the implementation it seemed that the grid elements were each a flex container, but even `flex-grow` didn't seem to work.

First realization: height percentage only takes the parent's height if it is specified. The rules seem to be quite elaborate, but that's the basic fact.

Second realization: streamlit likes to surround stuff with divs. So even though the grid square was a flex container, between my element there were a couple more divs, some flex containers and some display blocks. Why? beats me. That explained why `flex-grow` didn't work.

The first solution I found was a hack that used `::before` pseudo-element, padding and absolute positioning. It worked, but it was an ugly truth. After some more digging I found a newer property (2021) called `aspect-ratio` which conveniently does exactly what I wanted: keep the block square. It's sad though that it wasn't the first result on google.

So what did I learn? height is tricky? not sure, but it's interesting enough to note down. In the future, I need to up my web debugging game.

Anyway, that ended this tale, but many other woes followed, from which I will spare you, dear reader.