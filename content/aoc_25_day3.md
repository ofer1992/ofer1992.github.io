Title: AoC 2025 - Day 3
Date: 2025-12-03 12:54
Category: Programming
Status: published
Tags: aoc

Day 3 of AoC 2025. Following up on ![yesterday]({filename}/aoc_25_day2.md), today I'm gonna try to solve the question using typescript, but in a Jupyter notebook, writing along while programming. Today's input looks like this:


```typescript
import fs from "node:fs"
```


```typescript
const input = fs.readFileSync("input.txt", "utf-8")

console.log(input.split('\n').slice(0,3))
```

<pre class="ansi-output">
[
  <span class="ansi-green-fg">&#34;2215452689925244273244333436189317446384838478525478824435233342352236255624326767355438753493222423&#34;</span>,
  <span class="ansi-green-fg">&#34;1222232323222232132222323221226222225212221213232122232311152232223212123622111212223162322221323211&#34;</span>,
  <span class="ansi-green-fg">&#34;3786645737446363554463656544667372864465545434545435744345766553343446943531537627746253556233634463&#34;</span>
]

</pre>


```typescript
// sample input
const sample = `\
987654321111111
811111111111119
234234234234278
818181911112111\
`
console.log(sample)
```

<pre class="ansi-output">
987654321111111
811111111111119
234234234234278
818181911112111

</pre>

The first part asks as to choose in each row two digits that taken together form the largest number in that row. The two digits must maintain their left-to-right order. For example:
- in row 1: **98**7654321111111 forms 98
- in row 2: **8**1111111111111**9** forms 89
- in row 3: 2342342342342**78** forms 78
- in row 4: 818181**9**1111**2**111 forms 92

Then we sum them all and get


```typescript
98+89+78+92
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">357</span>
</pre>



which is the final answer. Some insights:
- the left digit dominates the size comparison
- the left digit will never be the last one, because there won't be room for the right digit
- if the same digit appears twice, it's always better to pick the left most one (only increase the right digit candidates this way)

Okay, so the algorithm will be as follows:
- `left_digit = max(row[:-1])`
- `right_digit = max(row[ind_left_digit:])`


```typescript
// the name jolt is a ref to the AoC lore in the question
function maxJolt(nums: number[]) {
  const lcand = nums.slice(0, -1)
  const ldigit = Math.max(...lcand)
  const lind = lcand.indexOf(ldigit)
  const rdigit = Math.max(...nums.slice(lind+1, nums.length))
  return ldigit * 10 + rdigit
}

function part1(input: string, debug=false) {
  let sum = 0;
  for (const r of input.split("\n")) {
    const res = maxJolt(r.split('').map(n => parseInt(n)))
    sum += res
    if (debug) {
      console.log(r)
      console.log(res)
      console.log(sum)
    }
  }
  return sum
}
```


```typescript
console.log(part1(sample, true))
```

<pre class="ansi-output">
987654321111111
<span class="ansi-yellow-fg">98</span>
<span class="ansi-yellow-fg">98</span>
811111111111119
<span class="ansi-yellow-fg">89</span>
<span class="ansi-yellow-fg">187</span>
234234234234278
<span class="ansi-yellow-fg">78</span>
<span class="ansi-yellow-fg">265</span>
818181911112111
<span class="ansi-yellow-fg">92</span>
<span class="ansi-yellow-fg">357</span>
<span class="ansi-yellow-fg">357</span>

</pre>

Looks good, let's try the full input


```typescript
console.log(part1(input))
```

<pre class="ansi-output">
<span class="ansi-yellow-fg">17346</span>

</pre>

And we were right! let's move on to part 2. This time I leave more intermediate cells so you can see sum of the incremental process. 

Now the twist is that instead of 2 digits we need to choose 12 digits the form the largest number! I think the same idea as before can be extended to the general case: `(i+1)_digit = max(row[i_digit: -(12-i)])`. Might be easier to just build the algorithm to be generic to the number of digits, then we can verify if we reproduce the same results.


```typescript
const r = "987654321111111"
const nums = r.split('').map(n => parseInt(n))
const digits = []
const n_digits = 2
let last_ind = -1
let i = n_digits - 1
nums
```




<pre class="ansi-output">
[
  <span class="ansi-yellow-fg">9</span>, <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">7</span>, <span class="ansi-yellow-fg">6</span>, <span class="ansi-yellow-fg">5</span>, <span class="ansi-yellow-fg">4</span>,
  <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">2</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>,
  <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>
]
</pre>



We'll add to digits one by one


```typescript
let slice = nums.slice(last_ind + 1, nums.length-i)
slice
```




<pre class="ansi-output">
[
  <span class="ansi-yellow-fg">9</span>, <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">7</span>, <span class="ansi-yellow-fg">6</span>, <span class="ansi-yellow-fg">5</span>, <span class="ansi-yellow-fg">4</span>,
  <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">2</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>,
  <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>
]
</pre>




```typescript
let digit = Math.max(...slice)
digits.push(digit)
digit
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">9</span>
</pre>




```typescript
last_ind = nums.slice(last_ind+1, nums.length).indexOf(digit)
last_ind
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">0</span>
</pre>




```typescript
i = i - 1
slice = nums.slice(last_ind + 1, nums.length-i)
slice
```




<pre class="ansi-output">
[
  <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">7</span>, <span class="ansi-yellow-fg">6</span>, <span class="ansi-yellow-fg">5</span>, <span class="ansi-yellow-fg">4</span>, <span class="ansi-yellow-fg">3</span>,
  <span class="ansi-yellow-fg">2</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>,
  <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>
]
</pre>




```typescript
digit = Math.max(...slice)
digits.push(digit)
digit
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">8</span>
</pre>




```typescript
digits
```




<pre class="ansi-output">
[ <span class="ansi-yellow-fg">9</span>, <span class="ansi-yellow-fg">8</span> ]
</pre>



Okay, so we kinda get how to body should work, let's merge it all, and try the 12 digits. Should get 987654321111


```typescript
const r = "987654321111111"
const nums = r.split('').map(n => parseInt(n))
const digits = []
const n_digits = 12
let last_ind = -1
// let i = n_digits - 1
for (let i = n_digits - 1; i >=0; i--) {
  const slice = nums.slice(last_ind + 1, nums.length-i)  
  const digit = Math.max(...slice)
  last_ind = last_ind + slice.indexOf(digit) + 1
  digits.push(digit)  
}
digits
```




<pre class="ansi-output">
[
  <span class="ansi-yellow-fg">9</span>, <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">7</span>, <span class="ansi-yellow-fg">6</span>, <span class="ansi-yellow-fg">5</span>,
  <span class="ansi-yellow-fg">4</span>, <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">2</span>, <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>,
  <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">1</span>
]
</pre>



To turn it into a number we can use reduce


```typescript
digits.reduce((s, x) => s*10 + x, 0)
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">987654321111</span>
</pre>



Looks good, let's put it in a function and try the rest of the sample


```typescript
function maxJolt2(nums, n_digits) {
  const digits = []
  let last_ind = -1
  for (let i = n_digits - 1; i >=0; i--) {
    const slice = nums.slice(last_ind + 1, nums.length-i)  
    const digit = Math.max(...slice)
    last_ind = last_ind + slice.indexOf(digit) + 1
    digits.push(digit)  
  }
  return digits.reduce((s, x) => s*10 + x, 0)
}
```


```typescript
let sum = 0
sample.split("\n").forEach(r => {
  const nums = r.split('').map(n => parseInt(n))
  const res = maxJolt2(nums, 12)
  console.log(res)
  sum += res
})
console.log(sum)
```

<pre class="ansi-output">
<span class="ansi-yellow-fg">987654321111</span>
<span class="ansi-yellow-fg">811111111119</span>
<span class="ansi-yellow-fg">434234234278</span>
<span class="ansi-yellow-fg">888911112111</span>
<span class="ansi-yellow-fg">3121910778619</span>

</pre>

Looks correct. Finally, let's put that in a function and finish


```typescript
function part2(input: string) {
  let sum = 0
  input.split("\n").forEach(r => {
    const nums = r.split('').map(n => parseInt(n))
    const res = maxJolt2(nums, 12)
    // console.log(res)
    sum += res
  })
  return sum
}

part2(input)
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">172981362045136</span>
</pre>



Success!

As a bonus, I want to see if we can rewrite maxJolt2 in a functional way. I'm thinking recursion


```typescript
function rMaxJolt2(nums, n_digits) {
  if (n_digits == 1) return Math.max(...nums);
  const digit = Math.max(...nums.slice(0, -n_digits + 1))
  return digit * 10**(n_digits - 1) + rMaxJolt2(nums.slice(nums.indexOf(digit) + 1, nums.length), n_digits - 1)
}

rMaxJolt2("818181911112111".split("").map(n => parseInt(n)), 12)
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">888911112111</span>
</pre>


