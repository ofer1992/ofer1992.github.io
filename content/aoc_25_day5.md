Title: AoC 2025 - Day 5
Date: 2025-12-05 11:18
Category: Programming
Status: published
Tags: aoc

```typescript
import fs from 'node:fs';
```


```typescript
const input = fs.readFileSync('input.txt', 'utf-8');
```


```typescript
const sample = `\
3-5
10-14
16-20
12-18

1
5
8
11
17
32`;
```

## Part 1

The first part of the input has a list of inclusive intervals, eg 3-5 for 3, 4, 5 etc. The second part has a list of numbers. We need to check how many of those are contained in the intervals. Approaches:

- naive: for each pair of interval and number check if number contained in interval.
    - O(r*n)
- sort the numbers, then for each interval check where the borders fall in the numbers array
    -  O(n) for the sort
    -  For each range we have O(log(n)) to find indexes of borders, so O(r*log(n)) in total.
    -  Add slice to set of seen numbers (are there repetitions). Now this in the worst case would be O(n) (imagine all the ranges contain all the numbers). We could solve it by removing the slice from the number array but then that incurs its own cost which I can't of the top of my head figure out.
- merge the ranges and then sort the borders and numbers together, keeping track of what is what. Then you just iterate on the combined array, noting when you are inside a range.
    -  Merge is O(r), sort is O(r+n), iteration is O(r+n). Probably the optimal solution.

Let's start with the naive just because it's the quickest, the input might be small enough, at least for part 1.


```typescript
const [interval_s, num_s] = sample.split("\n\n");
[interval_s, num_s];
```




<pre class="ansi-output">
[ <span class="ansi-green-fg">&#34;3-5\n10-14\n16-20\n12-18&#34;</span>, <span class="ansi-green-fg">&#34;1\n5\n8\n11\n17\n32&#34;</span> ]
</pre>




```typescript
const intervals = interval_s.split("\n").map(rs => rs.split("-").map(b => parseInt(b)));
intervals;
```




<pre class="ansi-output">
[ [ <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">5</span> ], [ <span class="ansi-yellow-fg">10</span>, <span class="ansi-yellow-fg">14</span> ], [ <span class="ansi-yellow-fg">16</span>, <span class="ansi-yellow-fg">20</span> ], [ <span class="ansi-yellow-fg">12</span>, <span class="ansi-yellow-fg">18</span> ] ]
</pre>




```typescript
const nums = num_s.split('\n').map(n => parseInt(n));
```


```typescript
function process(input: string) {
  const [interval_s, num_s] = input.split("\n\n");
  [interval_s, num_s];
  const intervals = interval_s.split("\n").map(rs => rs.split("-").map(b => parseInt(b)));
  intervals;
  const nums = num_s.split('\n').map(n => parseInt(n))
  return [intervals, nums]
}
```


```typescript
const [intervals, nums] = process(sample);
[intervals, nums];
```




<pre class="ansi-output">
[
  [ [ <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">5</span> ], [ <span class="ansi-yellow-fg">10</span>, <span class="ansi-yellow-fg">14</span> ], [ <span class="ansi-yellow-fg">16</span>, <span class="ansi-yellow-fg">20</span> ], [ <span class="ansi-yellow-fg">12</span>, <span class="ansi-yellow-fg">18</span> ] ],
  [ <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">5</span>, <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">11</span>, <span class="ansi-yellow-fg">17</span>, <span class="ansi-yellow-fg">32</span> ]
]
</pre>




```typescript
const n = 5;
intervals.some(i => i[0] <= n && n <= i[1]);
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">true</span>
</pre>




```typescript
nums.filter(n => intervals.some(i => i[0] <= n && n <= i[1]));
```




<pre class="ansi-output">
[ <span class="ansi-yellow-fg">5</span>, <span class="ansi-yellow-fg">11</span>, <span class="ansi-yellow-fg">17</span> ]
</pre>



Let's put it all in a function


```typescript
function part1(input: string) {
  const [intervals, nums] = process(input);
  return nums.filter(n => intervals.some(i => i[0] <= n && n <= i[1])).length;
}
part1(sample); // should be 3
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">3</span>
</pre>




```typescript
part1(input);
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">513</span>
</pre>



Okay, success. Let's move on

## Part 2

The next question is: how many numbers are covered by the ranges? so the numbers list is no longer relevant, but we need to handle the overlaps between the ranges. The naive way would be to just iterate over the ranges and add numbers to a set or something but that's wildly inefficient. The better way — let's sort and merge ranges.

I don't know if I ever sorted in js before, let's see what peculiarities are in store


```typescript
intervals.sort();
```




<pre class="ansi-output">
[ [ <span class="ansi-yellow-fg">10</span>, <span class="ansi-yellow-fg">14</span> ], [ <span class="ansi-yellow-fg">12</span>, <span class="ansi-yellow-fg">18</span> ], [ <span class="ansi-yellow-fg">16</span>, <span class="ansi-yellow-fg">20</span> ], [ <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">5</span> ] ]
</pre>



As expected. [Looking at the docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort) the default sort is something strange about converting to strings and sorting by the unicode code. Instead we need to supply a comparator function that returns (-1, 0, 1) for < = > cases.


```typescript
const a = 1;
const b = 2;
a < b ? -1 : a == b ?  0 : 1;
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">-1</span>
</pre>



Wait, looking more closesly at the docs, I see the actual requirement is not to return -1 or 1 exactly but a negative or positive value. This simplifies then to returning `a-b`


```typescript
const sorted = intervals.sort(([l1, r1], [l2, r2]) => l1 - l2);
sorted;
```




<pre class="ansi-output">
[ [ <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">5</span> ], [ <span class="ansi-yellow-fg">10</span>, <span class="ansi-yellow-fg">14</span> ], [ <span class="ansi-yellow-fg">12</span>, <span class="ansi-yellow-fg">18</span> ], [ <span class="ansi-yellow-fg">16</span>, <span class="ansi-yellow-fg">20</span> ] ]
</pre>



So how do we go about the merging? since we sorted, we know any overlap between an interval and the one on the right will be one of these forms:
```
l1   r1
l2      r2

l1      r1
  l2  r2
  
l1   r1
  l2      r2
```

So we merge by taking the larger of the `r` values and finish merging ones there is no more overlap. Let's test this out on the 3rd and 4th intervals in the sorted list which are overlapping


```typescript
// [12, 18], [16,20]
let [l, r] = sorted[2];
if (r < sorted[3][0]) console.log(`[${l}, ${r}] can be "commited"`)
r = Math.max(r, sorted[3][1]);
[l, r]
```




<pre class="ansi-output">
[ <span class="ansi-yellow-fg">12</span>, <span class="ansi-yellow-fg">20</span> ]
</pre>




```typescript
let [cur_l, cur_r] = sorted[0];
let s = 0;
sorted.forEach(([l, r]) => {
  console.log(cur_l, cur_r, l, r);
  if (cur_r < l) {
    s += cur_r - cur_l + 1; // length of inclusive range
    [cur_l, cur_r] = [l, r];
  }
  cur_r = Math.max(cur_r, r);
});
s += cur_r - cur_l + 1 // the last merged interval isn't added, possible bug here
```

<pre class="ansi-output">
<span class="ansi-yellow-fg">3</span> <span class="ansi-yellow-fg">5</span> <span class="ansi-yellow-fg">3</span> <span class="ansi-yellow-fg">5</span>
<span class="ansi-yellow-fg">3</span> <span class="ansi-yellow-fg">5</span> <span class="ansi-yellow-fg">10</span> <span class="ansi-yellow-fg">14</span>
<span class="ansi-yellow-fg">10</span> <span class="ansi-yellow-fg">14</span> <span class="ansi-yellow-fg">12</span> <span class="ansi-yellow-fg">18</span>
<span class="ansi-yellow-fg">10</span> <span class="ansi-yellow-fg">18</span> <span class="ansi-yellow-fg">16</span> <span class="ansi-yellow-fg">20</span>

</pre>




<pre class="ansi-output">
<span class="ansi-yellow-fg">14</span>
</pre>



Basically we don't even merge them, we just keep track of the count. Let's wrap everything up


```typescript
function part2(input: string) {
  const [intervals, _] = process(input);
  const sorted = intervals.sort(([l1, r1], [l2, r2]) => l1 - l2);
  let [cur_l, cur_r] = sorted[0];
  let s = 0;
  sorted.forEach(([l, r]) => {
    // console.log(cur_l, cur_r, l, r);
    if (cur_r < l) {
      s += cur_r - cur_l + 1; // length of inclusive range
      [cur_l, cur_r] = [l, r];
    }
    cur_r = Math.max(cur_r, r);
  });
  s += cur_r - cur_l + 1; // the last merged interval isn't added
  return s
}
```


```typescript
part2(sample)
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">14</span>
</pre>




```typescript
part2(input)
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">339668510830757</span>
</pre>



Success!
