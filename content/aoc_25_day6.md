Title: AoC 2025 - Day 6
Date: 2025-12-06 19:47
Category: Programming
Status: published
Tags: aoc


```typescript
import fs from "node:fs";
```


```typescript
const input = fs.readFileSync("input.txt", "utf-8");
```


```typescript
const sample = `\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  `;
```

## Part 1

In the first part of today, the input consists of 3 rows of space separated numbers and a row of space separated operators. We need to apply the operator on all the numbers in the column, so the challenge is to have everything aligned correctly. This begs for regexes.


```typescript
const rows = sample.split("\n");
```


```typescript
const num_pat = /\d+/g;
const op_pat = /[*+]/g;
```


```typescript
rows[0].match(num_pat).map(n => parseInt(n))
```




<pre class="ansi-output">
[ <span class="ansi-yellow-fg">123</span>, <span class="ansi-yellow-fg">328</span>, <span class="ansi-yellow-fg">51</span>, <span class="ansi-yellow-fg">64</span> ]
</pre>




```typescript
rows[3].match(op_pat)
```




<pre class="ansi-output">
[ <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span> ]
</pre>




```typescript
function process(input: string) {
  const rows = input.split("\n");
  const num_pat = /\d+/g;
  const op_pat = /[*+]/g;
  return [rows[0].match(num_pat).map(n => parseInt(n)),
          rows[1].match(num_pat).map(n => parseInt(n)),
          rows[2].match(num_pat).map(n => parseInt(n)),
          rows[3].match(op_pat)];
}
```


```typescript
const psample = process(sample);
psample
```




<pre class="ansi-output">
[
  [ <span class="ansi-yellow-fg">123</span>, <span class="ansi-yellow-fg">328</span>, <span class="ansi-yellow-fg">51</span>, <span class="ansi-yellow-fg">64</span> ],
  [ <span class="ansi-yellow-fg">45</span>, <span class="ansi-yellow-fg">64</span>, <span class="ansi-yellow-fg">387</span>, <span class="ansi-yellow-fg">23</span> ],
  [ <span class="ansi-yellow-fg">6</span>, <span class="ansi-yellow-fg">98</span>, <span class="ansi-yellow-fg">215</span>, <span class="ansi-yellow-fg">314</span> ],
  [ <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span> ]
]
</pre>




```typescript
const mat = psample;
const [h, w] = [mat.length, mat[0].length];
const tmat = [];
for (let c = 0; c < w; c++) {
  const nrow = [];
  for (let r = 0; r < h; r++) {
    nrow.push(mat[r][c]);
  }
  tmat.push(nrow);
}
tmat
```




<pre class="ansi-output">
[
  [ <span class="ansi-yellow-fg">123</span>, <span class="ansi-yellow-fg">45</span>, <span class="ansi-yellow-fg">6</span>, <span class="ansi-green-fg">&#34;*&#34;</span> ],
  [ <span class="ansi-yellow-fg">328</span>, <span class="ansi-yellow-fg">64</span>, <span class="ansi-yellow-fg">98</span>, <span class="ansi-green-fg">&#34;+&#34;</span> ],
  [ <span class="ansi-yellow-fg">51</span>, <span class="ansi-yellow-fg">387</span>, <span class="ansi-yellow-fg">215</span>, <span class="ansi-green-fg">&#34;*&#34;</span> ],
  [ <span class="ansi-yellow-fg">64</span>, <span class="ansi-yellow-fg">23</span>, <span class="ansi-yellow-fg">314</span>, <span class="ansi-green-fg">&#34;+&#34;</span> ]
]
</pre>



Let's write a reusable transpose function


```typescript
function transpose<T>(matrix: T[][]): T[][] {
  const [rows, cols] = [matrix.length, matrix[0].length];
  const transposed: T[][] = [];
  for (let c = 0; c < cols; c++) {
    const column: T[] = [];
    for (let r = 0; r < rows; r++) {
      column.push(matrix[r][c]);
    }
    transposed.push(column);
  }
  return transposed;
}
```


```typescript
const tsample = transpose(psample)
```

Let's create an obj that maps the operator string to lambdas. First, let me verify the reducer callback signature.


```typescript
console.log(tsample[0], tsample[0].slice(0, -1).reduce((r, x) => r * x))
```

<pre class="ansi-output">
[ <span class="ansi-yellow-fg">123</span>, <span class="ansi-yellow-fg">45</span>, <span class="ansi-yellow-fg">6</span>, <span class="ansi-green-fg">&#34;*&#34;</span> ] <span class="ansi-yellow-fg">33210</span>

</pre>


```typescript
const ops: Record<string, (acc: number, val: number) => number> = {
  "*": (acc, val) => acc * val,
  "+": (acc, val) => acc + val
}
ops
```


```typescript
tsample[0].slice(0, -1).reduce(ops[tsample[0][tsample[0].length-1]])
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">33210</span>
</pre>



Okay, this works now, let's make it clearer


```typescript
for (const row of tsample) {
  const nums = row.slice(0, -1);
  const op = row[row.length - 1];
  console.log(row, nums.reduce(ops[op]));
}
```

looks good. Let's wrap it up


```typescript
function part1(input: string): number {
  const processed = process(input);
  const transposed = transpose(processed);
  let result = 0;
  for (const row of transposed) {
    const nums = row.slice(0, -1);
    const op = row[row.length - 1];
    result += nums.reduce(ops[op]);
  }
  return result;
}
part1(sample);
```


```typescript
process(input)
```




<pre class="ansi-output">
[
  [
    <span class="ansi-yellow-fg">527</span>, <span class="ansi-yellow-fg">781</span>, <span class="ansi-yellow-fg">232</span>,  <span class="ansi-yellow-fg">95</span>,   <span class="ansi-yellow-fg">3</span>,   <span class="ansi-yellow-fg">75</span>,   <span class="ansi-yellow-fg">59</span>,  <span class="ansi-yellow-fg">66</span>,   <span class="ansi-yellow-fg">43</span>,  <span class="ansi-yellow-fg">5</span>,   <span class="ansi-yellow-fg">68</span>,  <span class="ansi-yellow-fg">877</span>,
     <span class="ansi-yellow-fg">31</span>,   <span class="ansi-yellow-fg">4</span>,  <span class="ansi-yellow-fg">54</span>, <span class="ansi-yellow-fg">914</span>,  <span class="ansi-yellow-fg">15</span>,   <span class="ansi-yellow-fg">22</span>,    <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">29</span>,    <span class="ansi-yellow-fg">4</span>, <span class="ansi-yellow-fg">17</span>,    <span class="ansi-yellow-fg">5</span>, <span class="ansi-yellow-fg">9176</span>,
      <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">885</span>,  <span class="ansi-yellow-fg">97</span>,  <span class="ansi-yellow-fg">88</span>,  <span class="ansi-yellow-fg">42</span>,    <span class="ansi-yellow-fg">6</span>,   <span class="ansi-yellow-fg">64</span>, <span class="ansi-yellow-fg">161</span>, <span class="ansi-yellow-fg">1675</span>, <span class="ansi-yellow-fg">36</span>,  <span class="ansi-yellow-fg">363</span>,  <span class="ansi-yellow-fg">738</span>,
     <span class="ansi-yellow-fg">71</span>, <span class="ansi-yellow-fg">224</span>, <span class="ansi-yellow-fg">453</span>,  <span class="ansi-yellow-fg">72</span>, <span class="ansi-yellow-fg">256</span>,  <span class="ansi-yellow-fg">594</span>,  <span class="ansi-yellow-fg">914</span>,  <span class="ansi-yellow-fg">97</span>,  <span class="ansi-yellow-fg">668</span>, <span class="ansi-yellow-fg">95</span>,  <span class="ansi-yellow-fg">723</span>,   <span class="ansi-yellow-fg">84</span>,
    <span class="ansi-yellow-fg">738</span>, <span class="ansi-yellow-fg">437</span>,  <span class="ansi-yellow-fg">38</span>,   <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">893</span>,  <span class="ansi-yellow-fg">416</span>,    <span class="ansi-yellow-fg">5</span>,  <span class="ansi-yellow-fg">21</span>,  <span class="ansi-yellow-fg">745</span>, <span class="ansi-yellow-fg">18</span>, <span class="ansi-yellow-fg">4566</span>,   <span class="ansi-yellow-fg">32</span>,
    <span class="ansi-yellow-fg">627</span>,  <span class="ansi-yellow-fg">16</span>,   <span class="ansi-yellow-fg">5</span>,  <span class="ansi-yellow-fg">45</span>,   <span class="ansi-yellow-fg">8</span>,   <span class="ansi-yellow-fg">88</span>, <span class="ansi-yellow-fg">4256</span>,  <span class="ansi-yellow-fg">52</span>,    <span class="ansi-yellow-fg">9</span>, <span class="ansi-yellow-fg">66</span>,  <span class="ansi-yellow-fg">317</span>,  <span class="ansi-yellow-fg">691</span>,
    <span class="ansi-yellow-fg">224</span>, <span class="ansi-yellow-fg">375</span>,  <span class="ansi-yellow-fg">17</span>,  <span class="ansi-yellow-fg">25</span>,   <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">3529</span>,   <span class="ansi-yellow-fg">42</span>,  <span class="ansi-yellow-fg">77</span>,   <span class="ansi-yellow-fg">86</span>,  <span class="ansi-yellow-fg">9</span>,    <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">865</span>,
    <span class="ansi-yellow-fg">793</span>,  <span class="ansi-yellow-fg">87</span>, <span class="ansi-yellow-fg">469</span>,  <span class="ansi-yellow-fg">86</span>, <span class="ansi-yellow-fg">452</span>,   <span class="ansi-yellow-fg">85</span>,   <span class="ansi-yellow-fg">51</span>,  <span class="ansi-yellow-fg">44</span>,   <span class="ansi-yellow-fg">11</span>, <span class="ansi-yellow-fg">43</span>,   <span class="ansi-yellow-fg">31</span>,   <span class="ansi-yellow-fg">22</span>,
     <span class="ansi-yellow-fg">15</span>,   <span class="ansi-yellow-fg">7</span>,  <span class="ansi-yellow-fg">42</span>,   <span class="ansi-yellow-fg">5</span>,
    ... 900 more items
  ],
  [
    <span class="ansi-yellow-fg">471</span>, <span class="ansi-yellow-fg">289</span>, <span class="ansi-yellow-fg">691</span>,  <span class="ansi-yellow-fg">56</span>,   <span class="ansi-yellow-fg">2</span>,   <span class="ansi-yellow-fg">16</span>,    <span class="ansi-yellow-fg">6</span>,  <span class="ansi-yellow-fg">47</span>,   <span class="ansi-yellow-fg">35</span>,    <span class="ansi-yellow-fg">3</span>,   <span class="ansi-yellow-fg">53</span>,  <span class="ansi-yellow-fg">959</span>,
     <span class="ansi-yellow-fg">91</span>,   <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">771</span>, <span class="ansi-yellow-fg">841</span>,  <span class="ansi-yellow-fg">49</span>,   <span class="ansi-yellow-fg">81</span>,  <span class="ansi-yellow-fg">644</span>, <span class="ansi-yellow-fg">459</span>,   <span class="ansi-yellow-fg">99</span>, <span class="ansi-yellow-fg">7874</span>,    <span class="ansi-yellow-fg">7</span>, <span class="ansi-yellow-fg">7994</span>,
     <span class="ansi-yellow-fg">29</span>, <span class="ansi-yellow-fg">993</span>,  <span class="ansi-yellow-fg">41</span>, <span class="ansi-yellow-fg">234</span>,  <span class="ansi-yellow-fg">34</span>,   <span class="ansi-yellow-fg">78</span>,  <span class="ansi-yellow-fg">142</span>, <span class="ansi-yellow-fg">146</span>, <span class="ansi-yellow-fg">5353</span>,   <span class="ansi-yellow-fg">46</span>,  <span class="ansi-yellow-fg">746</span>,  <span class="ansi-yellow-fg">939</span>,
     <span class="ansi-yellow-fg">54</span>, <span class="ansi-yellow-fg">596</span>,  <span class="ansi-yellow-fg">36</span>,  <span class="ansi-yellow-fg">11</span>, <span class="ansi-yellow-fg">551</span>,  <span class="ansi-yellow-fg">471</span>,   <span class="ansi-yellow-fg">29</span>,  <span class="ansi-yellow-fg">12</span>,  <span class="ansi-yellow-fg">477</span>,   <span class="ansi-yellow-fg">23</span>,  <span class="ansi-yellow-fg">415</span>,   <span class="ansi-yellow-fg">29</span>,
    <span class="ansi-yellow-fg">573</span>, <span class="ansi-yellow-fg">545</span>,  <span class="ansi-yellow-fg">16</span>,   <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">286</span>,  <span class="ansi-yellow-fg">429</span>,    <span class="ansi-yellow-fg">3</span>,  <span class="ansi-yellow-fg">49</span>,  <span class="ansi-yellow-fg">792</span>,   <span class="ansi-yellow-fg">38</span>, <span class="ansi-yellow-fg">3581</span>,   <span class="ansi-yellow-fg">68</span>,
    <span class="ansi-yellow-fg">557</span>, <span class="ansi-yellow-fg">694</span>,  <span class="ansi-yellow-fg">99</span>,  <span class="ansi-yellow-fg">23</span>,   <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">462</span>, <span class="ansi-yellow-fg">3287</span>,  <span class="ansi-yellow-fg">54</span>,   <span class="ansi-yellow-fg">82</span>,   <span class="ansi-yellow-fg">66</span>,  <span class="ansi-yellow-fg">585</span>,  <span class="ansi-yellow-fg">867</span>,
    <span class="ansi-yellow-fg">992</span>, <span class="ansi-yellow-fg">168</span>,  <span class="ansi-yellow-fg">49</span>,   <span class="ansi-yellow-fg">9</span>,  <span class="ansi-yellow-fg">39</span>, <span class="ansi-yellow-fg">6394</span>,  <span class="ansi-yellow-fg">572</span>, <span class="ansi-yellow-fg">738</span>,   <span class="ansi-yellow-fg">47</span>,   <span class="ansi-yellow-fg">63</span>,   <span class="ansi-yellow-fg">79</span>,   <span class="ansi-yellow-fg">11</span>,
    <span class="ansi-yellow-fg">994</span>, <span class="ansi-yellow-fg">787</span>, <span class="ansi-yellow-fg">928</span>,  <span class="ansi-yellow-fg">61</span>, <span class="ansi-yellow-fg">133</span>,   <span class="ansi-yellow-fg">17</span>,  <span class="ansi-yellow-fg">277</span>,  <span class="ansi-yellow-fg">64</span>,  <span class="ansi-yellow-fg">748</span>,   <span class="ansi-yellow-fg">75</span>,   <span class="ansi-yellow-fg">63</span>,   <span class="ansi-yellow-fg">63</span>,
     <span class="ansi-yellow-fg">28</span>,   <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">44</span>,  <span class="ansi-yellow-fg">12</span>,
    ... 900 more items
  ],
  [
    <span class="ansi-yellow-fg">527</span>,  <span class="ansi-yellow-fg">84</span>, <span class="ansi-yellow-fg">5159</span>,   <span class="ansi-yellow-fg">46</span>,  <span class="ansi-yellow-fg">96</span>,  <span class="ansi-yellow-fg">74</span>,    <span class="ansi-yellow-fg">9</span>,   <span class="ansi-yellow-fg">31</span>,    <span class="ansi-yellow-fg">1</span>,   <span class="ansi-yellow-fg">54</span>,   <span class="ansi-yellow-fg">93</span>, <span class="ansi-yellow-fg">2525</span>,
     <span class="ansi-yellow-fg">19</span>,  <span class="ansi-yellow-fg">87</span>,  <span class="ansi-yellow-fg">555</span>,  <span class="ansi-yellow-fg">328</span>,  <span class="ansi-yellow-fg">96</span>,  <span class="ansi-yellow-fg">13</span>,  <span class="ansi-yellow-fg">698</span>, <span class="ansi-yellow-fg">3168</span>,  <span class="ansi-yellow-fg">535</span>, <span class="ansi-yellow-fg">2246</span>,   <span class="ansi-yellow-fg">58</span>, <span class="ansi-yellow-fg">5345</span>,
     <span class="ansi-yellow-fg">63</span>, <span class="ansi-yellow-fg">297</span>,   <span class="ansi-yellow-fg">23</span>,  <span class="ansi-yellow-fg">235</span>,  <span class="ansi-yellow-fg">54</span>, <span class="ansi-yellow-fg">239</span>,  <span class="ansi-yellow-fg">445</span>,  <span class="ansi-yellow-fg">262</span>, <span class="ansi-yellow-fg">3591</span>,   <span class="ansi-yellow-fg">98</span>, <span class="ansi-yellow-fg">7913</span>,  <span class="ansi-yellow-fg">674</span>,
     <span class="ansi-yellow-fg">26</span>, <span class="ansi-yellow-fg">649</span>,    <span class="ansi-yellow-fg">9</span>,   <span class="ansi-yellow-fg">12</span>,  <span class="ansi-yellow-fg">82</span>, <span class="ansi-yellow-fg">329</span>,   <span class="ansi-yellow-fg">18</span>,   <span class="ansi-yellow-fg">45</span>,  <span class="ansi-yellow-fg">178</span>,    <span class="ansi-yellow-fg">3</span>,  <span class="ansi-yellow-fg">947</span>,   <span class="ansi-yellow-fg">65</span>,
    <span class="ansi-yellow-fg">715</span>,  <span class="ansi-yellow-fg">68</span>,   <span class="ansi-yellow-fg">47</span>,   <span class="ansi-yellow-fg">57</span>, <span class="ansi-yellow-fg">547</span>, <span class="ansi-yellow-fg">938</span>,    <span class="ansi-yellow-fg">1</span>,   <span class="ansi-yellow-fg">84</span>,  <span class="ansi-yellow-fg">653</span>,   <span class="ansi-yellow-fg">97</span>, <span class="ansi-yellow-fg">9138</span>,   <span class="ansi-yellow-fg">37</span>,
    <span class="ansi-yellow-fg">341</span>, <span class="ansi-yellow-fg">918</span>,   <span class="ansi-yellow-fg">14</span>, <span class="ansi-yellow-fg">4329</span>, <span class="ansi-yellow-fg">375</span>, <span class="ansi-yellow-fg">847</span>, <span class="ansi-yellow-fg">1118</span>,   <span class="ansi-yellow-fg">33</span>,   <span class="ansi-yellow-fg">99</span>,   <span class="ansi-yellow-fg">38</span>,  <span class="ansi-yellow-fg">773</span>,  <span class="ansi-yellow-fg">498</span>,
      <span class="ansi-yellow-fg">7</span>,  <span class="ansi-yellow-fg">11</span>,   <span class="ansi-yellow-fg">48</span>,    <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">65</span>, <span class="ansi-yellow-fg">246</span>,  <span class="ansi-yellow-fg">117</span>,  <span class="ansi-yellow-fg">358</span>,   <span class="ansi-yellow-fg">36</span>,   <span class="ansi-yellow-fg">14</span>,   <span class="ansi-yellow-fg">49</span>,   <span class="ansi-yellow-fg">26</span>,
     <span class="ansi-yellow-fg">46</span>, <span class="ansi-yellow-fg">638</span>,  <span class="ansi-yellow-fg">724</span>,   <span class="ansi-yellow-fg">67</span>, <span class="ansi-yellow-fg">382</span>,  <span class="ansi-yellow-fg">16</span>, <span class="ansi-yellow-fg">9749</span>,  <span class="ansi-yellow-fg">954</span>,  <span class="ansi-yellow-fg">725</span>,   <span class="ansi-yellow-fg">86</span>,   <span class="ansi-yellow-fg">17</span>,   <span class="ansi-yellow-fg">51</span>,
     <span class="ansi-yellow-fg">47</span>,  <span class="ansi-yellow-fg">38</span>,   <span class="ansi-yellow-fg">18</span>,   <span class="ansi-yellow-fg">42</span>,
    ... 900 more items
  ],
  <span class="ansi-bold">null</span>
]
</pre>




```typescript
part1(input);
```

<pre style="background-color: rgba(244, 67, 54, 0.28)">
Stack trace:
TypeError: Cannot read properties of null (reading &#39;0&#39;)
    at transpose (&lt;anonymous&gt;:10:23)
    at part1 (&lt;anonymous&gt;:3:14)
    at &lt;anonymous&gt;:1:22
</pre>

Okay, looking at the input there's actually more than 3 rows of numbers, let's fix the processing function


```typescript
[...[1,2,3],4] // checking if this works
```




<pre class="ansi-output">
[ <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">2</span>, <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">4</span> ]
</pre>




```typescript
function process(input: string) {
  const rows = input.split("\n");
  const num_pat = /\d+/g;
  const op_pat = /[*+]/g;
  return [...rows.slice(0, -1).map(r => r.match(num_pat).map(n => parseInt(n))),
          rows[rows.length - 1].match(op_pat)];
}
```


```typescript
process(input)
```




<pre class="ansi-output">
[
  [
    <span class="ansi-yellow-fg">527</span>, <span class="ansi-yellow-fg">781</span>, <span class="ansi-yellow-fg">232</span>,  <span class="ansi-yellow-fg">95</span>,   <span class="ansi-yellow-fg">3</span>,   <span class="ansi-yellow-fg">75</span>,   <span class="ansi-yellow-fg">59</span>,  <span class="ansi-yellow-fg">66</span>,   <span class="ansi-yellow-fg">43</span>,  <span class="ansi-yellow-fg">5</span>,   <span class="ansi-yellow-fg">68</span>,  <span class="ansi-yellow-fg">877</span>,
     <span class="ansi-yellow-fg">31</span>,   <span class="ansi-yellow-fg">4</span>,  <span class="ansi-yellow-fg">54</span>, <span class="ansi-yellow-fg">914</span>,  <span class="ansi-yellow-fg">15</span>,   <span class="ansi-yellow-fg">22</span>,    <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">29</span>,    <span class="ansi-yellow-fg">4</span>, <span class="ansi-yellow-fg">17</span>,    <span class="ansi-yellow-fg">5</span>, <span class="ansi-yellow-fg">9176</span>,
      <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">885</span>,  <span class="ansi-yellow-fg">97</span>,  <span class="ansi-yellow-fg">88</span>,  <span class="ansi-yellow-fg">42</span>,    <span class="ansi-yellow-fg">6</span>,   <span class="ansi-yellow-fg">64</span>, <span class="ansi-yellow-fg">161</span>, <span class="ansi-yellow-fg">1675</span>, <span class="ansi-yellow-fg">36</span>,  <span class="ansi-yellow-fg">363</span>,  <span class="ansi-yellow-fg">738</span>,
     <span class="ansi-yellow-fg">71</span>, <span class="ansi-yellow-fg">224</span>, <span class="ansi-yellow-fg">453</span>,  <span class="ansi-yellow-fg">72</span>, <span class="ansi-yellow-fg">256</span>,  <span class="ansi-yellow-fg">594</span>,  <span class="ansi-yellow-fg">914</span>,  <span class="ansi-yellow-fg">97</span>,  <span class="ansi-yellow-fg">668</span>, <span class="ansi-yellow-fg">95</span>,  <span class="ansi-yellow-fg">723</span>,   <span class="ansi-yellow-fg">84</span>,
    <span class="ansi-yellow-fg">738</span>, <span class="ansi-yellow-fg">437</span>,  <span class="ansi-yellow-fg">38</span>,   <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">893</span>,  <span class="ansi-yellow-fg">416</span>,    <span class="ansi-yellow-fg">5</span>,  <span class="ansi-yellow-fg">21</span>,  <span class="ansi-yellow-fg">745</span>, <span class="ansi-yellow-fg">18</span>, <span class="ansi-yellow-fg">4566</span>,   <span class="ansi-yellow-fg">32</span>,
    <span class="ansi-yellow-fg">627</span>,  <span class="ansi-yellow-fg">16</span>,   <span class="ansi-yellow-fg">5</span>,  <span class="ansi-yellow-fg">45</span>,   <span class="ansi-yellow-fg">8</span>,   <span class="ansi-yellow-fg">88</span>, <span class="ansi-yellow-fg">4256</span>,  <span class="ansi-yellow-fg">52</span>,    <span class="ansi-yellow-fg">9</span>, <span class="ansi-yellow-fg">66</span>,  <span class="ansi-yellow-fg">317</span>,  <span class="ansi-yellow-fg">691</span>,
    <span class="ansi-yellow-fg">224</span>, <span class="ansi-yellow-fg">375</span>,  <span class="ansi-yellow-fg">17</span>,  <span class="ansi-yellow-fg">25</span>,   <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">3529</span>,   <span class="ansi-yellow-fg">42</span>,  <span class="ansi-yellow-fg">77</span>,   <span class="ansi-yellow-fg">86</span>,  <span class="ansi-yellow-fg">9</span>,    <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">865</span>,
    <span class="ansi-yellow-fg">793</span>,  <span class="ansi-yellow-fg">87</span>, <span class="ansi-yellow-fg">469</span>,  <span class="ansi-yellow-fg">86</span>, <span class="ansi-yellow-fg">452</span>,   <span class="ansi-yellow-fg">85</span>,   <span class="ansi-yellow-fg">51</span>,  <span class="ansi-yellow-fg">44</span>,   <span class="ansi-yellow-fg">11</span>, <span class="ansi-yellow-fg">43</span>,   <span class="ansi-yellow-fg">31</span>,   <span class="ansi-yellow-fg">22</span>,
     <span class="ansi-yellow-fg">15</span>,   <span class="ansi-yellow-fg">7</span>,  <span class="ansi-yellow-fg">42</span>,   <span class="ansi-yellow-fg">5</span>,
    ... 900 more items
  ],
  [
    <span class="ansi-yellow-fg">471</span>, <span class="ansi-yellow-fg">289</span>, <span class="ansi-yellow-fg">691</span>,  <span class="ansi-yellow-fg">56</span>,   <span class="ansi-yellow-fg">2</span>,   <span class="ansi-yellow-fg">16</span>,    <span class="ansi-yellow-fg">6</span>,  <span class="ansi-yellow-fg">47</span>,   <span class="ansi-yellow-fg">35</span>,    <span class="ansi-yellow-fg">3</span>,   <span class="ansi-yellow-fg">53</span>,  <span class="ansi-yellow-fg">959</span>,
     <span class="ansi-yellow-fg">91</span>,   <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">771</span>, <span class="ansi-yellow-fg">841</span>,  <span class="ansi-yellow-fg">49</span>,   <span class="ansi-yellow-fg">81</span>,  <span class="ansi-yellow-fg">644</span>, <span class="ansi-yellow-fg">459</span>,   <span class="ansi-yellow-fg">99</span>, <span class="ansi-yellow-fg">7874</span>,    <span class="ansi-yellow-fg">7</span>, <span class="ansi-yellow-fg">7994</span>,
     <span class="ansi-yellow-fg">29</span>, <span class="ansi-yellow-fg">993</span>,  <span class="ansi-yellow-fg">41</span>, <span class="ansi-yellow-fg">234</span>,  <span class="ansi-yellow-fg">34</span>,   <span class="ansi-yellow-fg">78</span>,  <span class="ansi-yellow-fg">142</span>, <span class="ansi-yellow-fg">146</span>, <span class="ansi-yellow-fg">5353</span>,   <span class="ansi-yellow-fg">46</span>,  <span class="ansi-yellow-fg">746</span>,  <span class="ansi-yellow-fg">939</span>,
     <span class="ansi-yellow-fg">54</span>, <span class="ansi-yellow-fg">596</span>,  <span class="ansi-yellow-fg">36</span>,  <span class="ansi-yellow-fg">11</span>, <span class="ansi-yellow-fg">551</span>,  <span class="ansi-yellow-fg">471</span>,   <span class="ansi-yellow-fg">29</span>,  <span class="ansi-yellow-fg">12</span>,  <span class="ansi-yellow-fg">477</span>,   <span class="ansi-yellow-fg">23</span>,  <span class="ansi-yellow-fg">415</span>,   <span class="ansi-yellow-fg">29</span>,
    <span class="ansi-yellow-fg">573</span>, <span class="ansi-yellow-fg">545</span>,  <span class="ansi-yellow-fg">16</span>,   <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">286</span>,  <span class="ansi-yellow-fg">429</span>,    <span class="ansi-yellow-fg">3</span>,  <span class="ansi-yellow-fg">49</span>,  <span class="ansi-yellow-fg">792</span>,   <span class="ansi-yellow-fg">38</span>, <span class="ansi-yellow-fg">3581</span>,   <span class="ansi-yellow-fg">68</span>,
    <span class="ansi-yellow-fg">557</span>, <span class="ansi-yellow-fg">694</span>,  <span class="ansi-yellow-fg">99</span>,  <span class="ansi-yellow-fg">23</span>,   <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">462</span>, <span class="ansi-yellow-fg">3287</span>,  <span class="ansi-yellow-fg">54</span>,   <span class="ansi-yellow-fg">82</span>,   <span class="ansi-yellow-fg">66</span>,  <span class="ansi-yellow-fg">585</span>,  <span class="ansi-yellow-fg">867</span>,
    <span class="ansi-yellow-fg">992</span>, <span class="ansi-yellow-fg">168</span>,  <span class="ansi-yellow-fg">49</span>,   <span class="ansi-yellow-fg">9</span>,  <span class="ansi-yellow-fg">39</span>, <span class="ansi-yellow-fg">6394</span>,  <span class="ansi-yellow-fg">572</span>, <span class="ansi-yellow-fg">738</span>,   <span class="ansi-yellow-fg">47</span>,   <span class="ansi-yellow-fg">63</span>,   <span class="ansi-yellow-fg">79</span>,   <span class="ansi-yellow-fg">11</span>,
    <span class="ansi-yellow-fg">994</span>, <span class="ansi-yellow-fg">787</span>, <span class="ansi-yellow-fg">928</span>,  <span class="ansi-yellow-fg">61</span>, <span class="ansi-yellow-fg">133</span>,   <span class="ansi-yellow-fg">17</span>,  <span class="ansi-yellow-fg">277</span>,  <span class="ansi-yellow-fg">64</span>,  <span class="ansi-yellow-fg">748</span>,   <span class="ansi-yellow-fg">75</span>,   <span class="ansi-yellow-fg">63</span>,   <span class="ansi-yellow-fg">63</span>,
     <span class="ansi-yellow-fg">28</span>,   <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">44</span>,  <span class="ansi-yellow-fg">12</span>,
    ... 900 more items
  ],
  [
    <span class="ansi-yellow-fg">527</span>,  <span class="ansi-yellow-fg">84</span>, <span class="ansi-yellow-fg">5159</span>,   <span class="ansi-yellow-fg">46</span>,  <span class="ansi-yellow-fg">96</span>,  <span class="ansi-yellow-fg">74</span>,    <span class="ansi-yellow-fg">9</span>,   <span class="ansi-yellow-fg">31</span>,    <span class="ansi-yellow-fg">1</span>,   <span class="ansi-yellow-fg">54</span>,   <span class="ansi-yellow-fg">93</span>, <span class="ansi-yellow-fg">2525</span>,
     <span class="ansi-yellow-fg">19</span>,  <span class="ansi-yellow-fg">87</span>,  <span class="ansi-yellow-fg">555</span>,  <span class="ansi-yellow-fg">328</span>,  <span class="ansi-yellow-fg">96</span>,  <span class="ansi-yellow-fg">13</span>,  <span class="ansi-yellow-fg">698</span>, <span class="ansi-yellow-fg">3168</span>,  <span class="ansi-yellow-fg">535</span>, <span class="ansi-yellow-fg">2246</span>,   <span class="ansi-yellow-fg">58</span>, <span class="ansi-yellow-fg">5345</span>,
     <span class="ansi-yellow-fg">63</span>, <span class="ansi-yellow-fg">297</span>,   <span class="ansi-yellow-fg">23</span>,  <span class="ansi-yellow-fg">235</span>,  <span class="ansi-yellow-fg">54</span>, <span class="ansi-yellow-fg">239</span>,  <span class="ansi-yellow-fg">445</span>,  <span class="ansi-yellow-fg">262</span>, <span class="ansi-yellow-fg">3591</span>,   <span class="ansi-yellow-fg">98</span>, <span class="ansi-yellow-fg">7913</span>,  <span class="ansi-yellow-fg">674</span>,
     <span class="ansi-yellow-fg">26</span>, <span class="ansi-yellow-fg">649</span>,    <span class="ansi-yellow-fg">9</span>,   <span class="ansi-yellow-fg">12</span>,  <span class="ansi-yellow-fg">82</span>, <span class="ansi-yellow-fg">329</span>,   <span class="ansi-yellow-fg">18</span>,   <span class="ansi-yellow-fg">45</span>,  <span class="ansi-yellow-fg">178</span>,    <span class="ansi-yellow-fg">3</span>,  <span class="ansi-yellow-fg">947</span>,   <span class="ansi-yellow-fg">65</span>,
    <span class="ansi-yellow-fg">715</span>,  <span class="ansi-yellow-fg">68</span>,   <span class="ansi-yellow-fg">47</span>,   <span class="ansi-yellow-fg">57</span>, <span class="ansi-yellow-fg">547</span>, <span class="ansi-yellow-fg">938</span>,    <span class="ansi-yellow-fg">1</span>,   <span class="ansi-yellow-fg">84</span>,  <span class="ansi-yellow-fg">653</span>,   <span class="ansi-yellow-fg">97</span>, <span class="ansi-yellow-fg">9138</span>,   <span class="ansi-yellow-fg">37</span>,
    <span class="ansi-yellow-fg">341</span>, <span class="ansi-yellow-fg">918</span>,   <span class="ansi-yellow-fg">14</span>, <span class="ansi-yellow-fg">4329</span>, <span class="ansi-yellow-fg">375</span>, <span class="ansi-yellow-fg">847</span>, <span class="ansi-yellow-fg">1118</span>,   <span class="ansi-yellow-fg">33</span>,   <span class="ansi-yellow-fg">99</span>,   <span class="ansi-yellow-fg">38</span>,  <span class="ansi-yellow-fg">773</span>,  <span class="ansi-yellow-fg">498</span>,
      <span class="ansi-yellow-fg">7</span>,  <span class="ansi-yellow-fg">11</span>,   <span class="ansi-yellow-fg">48</span>,    <span class="ansi-yellow-fg">2</span>,  <span class="ansi-yellow-fg">65</span>, <span class="ansi-yellow-fg">246</span>,  <span class="ansi-yellow-fg">117</span>,  <span class="ansi-yellow-fg">358</span>,   <span class="ansi-yellow-fg">36</span>,   <span class="ansi-yellow-fg">14</span>,   <span class="ansi-yellow-fg">49</span>,   <span class="ansi-yellow-fg">26</span>,
     <span class="ansi-yellow-fg">46</span>, <span class="ansi-yellow-fg">638</span>,  <span class="ansi-yellow-fg">724</span>,   <span class="ansi-yellow-fg">67</span>, <span class="ansi-yellow-fg">382</span>,  <span class="ansi-yellow-fg">16</span>, <span class="ansi-yellow-fg">9749</span>,  <span class="ansi-yellow-fg">954</span>,  <span class="ansi-yellow-fg">725</span>,   <span class="ansi-yellow-fg">86</span>,   <span class="ansi-yellow-fg">17</span>,   <span class="ansi-yellow-fg">51</span>,
     <span class="ansi-yellow-fg">47</span>,  <span class="ansi-yellow-fg">38</span>,   <span class="ansi-yellow-fg">18</span>,   <span class="ansi-yellow-fg">42</span>,
    ... 900 more items
  ],
  [
     <span class="ansi-yellow-fg">96</span>,   <span class="ansi-yellow-fg">7</span>, <span class="ansi-yellow-fg">9932</span>,   <span class="ansi-yellow-fg">96</span>,  <span class="ansi-yellow-fg">25</span>,  <span class="ansi-yellow-fg">77</span>,    <span class="ansi-yellow-fg">3</span>,    <span class="ansi-yellow-fg">6</span>,   <span class="ansi-yellow-fg">1</span>,  <span class="ansi-yellow-fg">198</span>,   <span class="ansi-yellow-fg">33</span>, <span class="ansi-yellow-fg">1758</span>,
     <span class="ansi-yellow-fg">64</span>,  <span class="ansi-yellow-fg">99</span>,  <span class="ansi-yellow-fg">928</span>, <span class="ansi-yellow-fg">1738</span>,   <span class="ansi-yellow-fg">8</span>,  <span class="ansi-yellow-fg">73</span>,  <span class="ansi-yellow-fg">373</span>, <span class="ansi-yellow-fg">4115</span>, <span class="ansi-yellow-fg">531</span>, <span class="ansi-yellow-fg">6283</span>,   <span class="ansi-yellow-fg">86</span>,   <span class="ansi-yellow-fg">71</span>,
     <span class="ansi-yellow-fg">66</span>, <span class="ansi-yellow-fg">442</span>,   <span class="ansi-yellow-fg">58</span>,  <span class="ansi-yellow-fg">525</span>,   <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">328</span>, <span class="ansi-yellow-fg">8563</span>,  <span class="ansi-yellow-fg">461</span>, <span class="ansi-yellow-fg">662</span>,    <span class="ansi-yellow-fg">6</span>, <span class="ansi-yellow-fg">9546</span>,  <span class="ansi-yellow-fg">295</span>,
     <span class="ansi-yellow-fg">33</span>, <span class="ansi-yellow-fg">662</span>,    <span class="ansi-yellow-fg">2</span>,   <span class="ansi-yellow-fg">32</span>,  <span class="ansi-yellow-fg">95</span>,   <span class="ansi-yellow-fg">5</span>,   <span class="ansi-yellow-fg">25</span>,   <span class="ansi-yellow-fg">96</span>,  <span class="ansi-yellow-fg">58</span>,    <span class="ansi-yellow-fg">3</span>,  <span class="ansi-yellow-fg">921</span>,   <span class="ansi-yellow-fg">72</span>,
    <span class="ansi-yellow-fg">783</span>,  <span class="ansi-yellow-fg">92</span>,   <span class="ansi-yellow-fg">11</span>,   <span class="ansi-yellow-fg">71</span>,   <span class="ansi-yellow-fg">1</span>,  <span class="ansi-yellow-fg">81</span>,   <span class="ansi-yellow-fg">51</span>,   <span class="ansi-yellow-fg">41</span>,  <span class="ansi-yellow-fg">28</span>,    <span class="ansi-yellow-fg">8</span>, <span class="ansi-yellow-fg">9666</span>,    <span class="ansi-yellow-fg">5</span>,
     <span class="ansi-yellow-fg">78</span>, <span class="ansi-yellow-fg">743</span>,   <span class="ansi-yellow-fg">11</span>, <span class="ansi-yellow-fg">2264</span>, <span class="ansi-yellow-fg">995</span>, <span class="ansi-yellow-fg">244</span>,   <span class="ansi-yellow-fg">74</span>,   <span class="ansi-yellow-fg">27</span>,  <span class="ansi-yellow-fg">32</span>,   <span class="ansi-yellow-fg">64</span>,   <span class="ansi-yellow-fg">62</span>,   <span class="ansi-yellow-fg">42</span>,
      <span class="ansi-yellow-fg">3</span>,  <span class="ansi-yellow-fg">83</span>,   <span class="ansi-yellow-fg">52</span>,    <span class="ansi-yellow-fg">1</span>,  <span class="ansi-yellow-fg">86</span>, <span class="ansi-yellow-fg">119</span>,  <span class="ansi-yellow-fg">234</span>,  <span class="ansi-yellow-fg">981</span>,   <span class="ansi-yellow-fg">9</span>,   <span class="ansi-yellow-fg">85</span>,   <span class="ansi-yellow-fg">55</span>,    <span class="ansi-yellow-fg">8</span>,
     <span class="ansi-yellow-fg">27</span>, <span class="ansi-yellow-fg">622</span>,  <span class="ansi-yellow-fg">225</span>,    <span class="ansi-yellow-fg">4</span>,  <span class="ansi-yellow-fg">98</span>,  <span class="ansi-yellow-fg">77</span>, <span class="ansi-yellow-fg">4974</span>, <span class="ansi-yellow-fg">7215</span>, <span class="ansi-yellow-fg">491</span>,   <span class="ansi-yellow-fg">37</span>,   <span class="ansi-yellow-fg">24</span>,   <span class="ansi-yellow-fg">75</span>,
      <span class="ansi-yellow-fg">5</span>, <span class="ansi-yellow-fg">383</span>,    <span class="ansi-yellow-fg">5</span>,   <span class="ansi-yellow-fg">81</span>,
    ... 900 more items
  ],
  [
    <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>,
    <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>,
    <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>,
    <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>,
    <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>,
    <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>,
    <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>,
    <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>,
    <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span>,
    ... 900 more items
  ]
]
</pre>




```typescript
part1(input);
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">5335495999141</span>
</pre>



correct!

## Part 2

Now we need to parse the input in a different way, instead of parsing row by row we need to parse column by column.


```typescript
input.split("\n").map(r => r.length)
```




<pre class="ansi-output">
[ <span class="ansi-yellow-fg">3708</span>, <span class="ansi-yellow-fg">3708</span>, <span class="ansi-yellow-fg">3708</span>, <span class="ansi-yellow-fg">3708</span>, <span class="ansi-yellow-fg">3708</span> ]
</pre>



So the input is rectangular/matrix. We can try to use the transpose function, since it will be easier to parse the numbers by rows like in the first part.


```typescript
const processedSample = transpose(sample.split("\n"));
processedSample.slice(0, 8);
```

Each row now has a number, the last column has the operator. A batdh of numbers is now seperated by a blank line. It would be nice if we could batch the lines by this separator then figure out from the last column the op and drop it and parse the numbers. Let's start with trying to "collect" the rows


```typescript
const tmp = psample[3];
```


```typescript
const sep = "    ";
console.log(psample[3], psample[3].join('') === sep)
```

<pre class="ansi-output">
[ <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">true</span>

</pre>


```typescript
for (const r of psample) {
  console.log(r, r.join('') === sep)
}
```

<pre class="ansi-output">
[ <span class="ansi-green-fg">&#34;1&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34;2&#34;</span>, <span class="ansi-green-fg">&#34;4&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34;3&#34;</span>, <span class="ansi-green-fg">&#34;5&#34;</span>, <span class="ansi-green-fg">&#34;6&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">true</span>
[ <span class="ansi-green-fg">&#34;3&#34;</span>, <span class="ansi-green-fg">&#34;6&#34;</span>, <span class="ansi-green-fg">&#34;9&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34;2&#34;</span>, <span class="ansi-green-fg">&#34;4&#34;</span>, <span class="ansi-green-fg">&#34;8&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34;8&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">true</span>
[ <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34;3&#34;</span>, <span class="ansi-green-fg">&#34;2&#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34;5&#34;</span>, <span class="ansi-green-fg">&#34;8&#34;</span>, <span class="ansi-green-fg">&#34;1&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34;1&#34;</span>, <span class="ansi-green-fg">&#34;7&#34;</span>, <span class="ansi-green-fg">&#34;5&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">true</span>
[ <span class="ansi-green-fg">&#34;6&#34;</span>, <span class="ansi-green-fg">&#34;2&#34;</span>, <span class="ansi-green-fg">&#34;3&#34;</span>, <span class="ansi-green-fg">&#34;+&#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34;4&#34;</span>, <span class="ansi-green-fg">&#34;3&#34;</span>, <span class="ansi-green-fg">&#34;1&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">false</span>
[ <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34;4&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ] <span class="ansi-yellow-fg">false</span>

</pre>

Seems to work. Now let's see how we can right the "chunker" function using reduce.


```typescript
[1,2,3,0,1,2,3,4,0,5].reduce((r, x) => {
  x === 0 ? r.push([]) : r[r.length - 1].push(x);
  return r;
}, [[]])
```




<pre class="ansi-output">
[ [ <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">2</span>, <span class="ansi-yellow-fg">3</span> ], [ <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">2</span>, <span class="ansi-yellow-fg">3</span>, <span class="ansi-yellow-fg">4</span> ], [ <span class="ansi-yellow-fg">5</span> ] ]
</pre>



Nice, js can be quite succinct with functional style. And now in our case


```typescript
function chunker(rows: string[][]): string[][][] {
  return rows.reduce((chunks, row) => {
    row.join('').trim() === "" ? chunks.push([]) : chunks[chunks.length - 1].push(row);
    return chunks;
  }, [[]] as string[][][])
}

const chunks = chunker(processedSample);
chunks;
```

Finally, let's see how we process a chunk


```typescript
const chunk = chunks[0];
chunk
```




<pre class="ansi-output">
[
  [ <span class="ansi-green-fg">&#34;1&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34;*&#34;</span> ],
  [ <span class="ansi-green-fg">&#34;2&#34;</span>, <span class="ansi-green-fg">&#34;4&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ],
  [ <span class="ansi-green-fg">&#34;3&#34;</span>, <span class="ansi-green-fg">&#34;5&#34;</span>, <span class="ansi-green-fg">&#34;6&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ]
]
</pre>




```typescript
const tchunk = transpose(chunk)
tchunk
```




<pre class="ansi-output">
[
  [ <span class="ansi-green-fg">&#34;1&#34;</span>, <span class="ansi-green-fg">&#34;2&#34;</span>, <span class="ansi-green-fg">&#34;3&#34;</span> ],
  [ <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34;4&#34;</span>, <span class="ansi-green-fg">&#34;5&#34;</span> ],
  [ <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34;6&#34;</span> ],
  [ <span class="ansi-green-fg">&#34;*&#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span>, <span class="ansi-green-fg">&#34; &#34;</span> ]
]
</pre>




```typescript
const op = tchunk[tchunk.length - 1].join('').trim()
op
```




<pre class="ansi-output">
<span class="ansi-green-fg">&#34;*&#34;</span>
</pre>



cool, and the numbers


```typescript
parseInt(chunk[0].slice(0, -1).join('').trim())
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">1</span>
</pre>




```typescript
chunk.map(r => parseInt(r.slice(0, -1).join('').trim()))
```




<pre class="ansi-output">
[ <span class="ansi-yellow-fg">1</span>, <span class="ansi-yellow-fg">24</span>, <span class="ansi-yellow-fg">356</span> ]
</pre>



Cool, the rest is like the last part, let's merge to one function


```typescript
function process_chunk(chunk: string[][]): number {
  const transposedChunk = transpose(chunk);
  const op = transposedChunk[transposedChunk.length - 1].join('').trim();
  const nums = chunk.map(row => parseInt(row.slice(0, -1).join('').trim()));
  return nums.reduce(ops[op]);
}
```

Let's verify on sample. According to the problem page, we should have 
1058 + 3253600 + 625 + 8544 = 3263827.


```typescript
chunks.map(c => process_chunk(c))
```




<pre class="ansi-output">
[ <span class="ansi-yellow-fg">8544</span>, <span class="ansi-yellow-fg">625</span>, <span class="ansi-yellow-fg">3253600</span>, <span class="ansi-yellow-fg">1058</span> ]
</pre>



Looks good. Let's finish this


```typescript
[1,2,3].reduce((acc, x) => acc + x)
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">6</span>
</pre>




```typescript
function part2(input: string): number {
  const transposedInput = transpose(input.split('\n'));
  const chunks = chunker(transposedInput);
  return chunks.map(chunk => process_chunk(chunk)).reduce((acc, val) => acc + val);
}

part2(sample)
```


```typescript
part2(input)
```




<pre class="ansi-output">
<span class="ansi-yellow-fg">10142723156431</span>
</pre>



Correct!
