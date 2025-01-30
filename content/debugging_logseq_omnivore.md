Title: Debugging session: Logseq Omnivore plugin
Date: 2024-07-22 14:24
Category: Dailies
Status: published

I'm trying to debug a weird issue with the Logseq omnivore plugin where it takes forever to sync and it seemingly creates and deletes pages needlessly.

My first step was to properly setting up a dev env (`pnpm dev`) which didn't work out of the box, instead of just building and printing (too old for this haha). After fiddling with configs for about an hour, I solved it by moving `index.html` out of `public/` into the root folder.

Now that dev was working, I could debug normally. The main culprit seems to be `fetchOmnivore`. It's a long function that seems to fetch everything. But even when I neuter it I still get the page creation syndrome.

Aha, but when I comment out the page deleting mechanism I get some more interesting results. Let's look at the code

```ts
    // delete blocks where article has been deleted from omnivore
    for (let after = 0; ; after += size) {
      const [deletedItems, hasNextPage] = await getDeletedOmnivoreItems(
        apiKey,
        after,
        size,
        parseDateTime(syncAt).toISO(),
        endpoint
      )
      for (const deletedItem of deletedItems) {
        if (!isSinglePage) {
          pageName = renderPageName(
            deletedItem,
            pageNameTemplate,
            preferredDateFormat
          )
          targetBlockId = await getOmnivoreBlockIdentity(pageName, blockTitle)

          // delete page if article is synced to a separate page and page is not a journal
          const existingPage = await logseq.Editor.getPage(pageName)
          if (existingPage && !existingPage['journal?']) {
            await logseq.Editor.deletePage(pageName)
            continue
          }
        }

        const existingBlock = await getBlockByContent(
          pageName,
          targetBlockId,
          deletedItem.slug
        )

        if (existingBlock) {
          await logseq.Editor.removeBlock(existingBlock.uuid)
        }
      }

      if (!hasNextPage) {
        break
      }
    }
```
When I removed the commenting, the phenomena didn't reproduce. Why? I had a guess: you can see that `getDeletedOmnivoreItems` is passed a syncDate argument. That means the first time you sync it will sync all of the pages. After a successful sync it won't happen again, since it only checks for pages after that date.

But why does this seem to always happen when I use the plugin? because there is some article in my db that is causing it. And it is “Mapping the Mind of a Large Language Model \ Anthropic”! The bad news are, I can't access it from the app, because it's too old!!! maybe I can do an API call? anyway, regardless this shouldn't crash the code. But first things first.

Starting with the needless page creation. The call to `getOmnivoreBlockIdentity` triggers it, in which in turn the call to `getOmnivorePage` triggers it, and in `getOmnivorePage` we have
```ts
  const omnivorePage = await logseq.Editor.getPage(pageName)
  if (omnivorePage) {
    return omnivorePage
  }

  const newOmnivorePage = await logseq.Editor.createPage(pageName, undefined, {
    createFirstBlock: false,
  })
```
So this creates a new page. Clearly undesirable behavior when we intend to delete that page in the first place!!

I ended up moving the call to `getOmnivoreBlockIdentity` outside of the if statement and wrapped the rest of the code with an else. [Here's the PR](https://github.com/omnivore-app/logseq-omnivore/pull/194).

So in total the problems I found:
- Pages to be deleted accidentally created before.
- I have a deleted article with a `\` (backslash?) and it crashed the deleting code before the change I did.
- I have a deleted article with an identical name to an existing article so it deletes the article I actually want to keep. Fixed by changing the deleted article's name.