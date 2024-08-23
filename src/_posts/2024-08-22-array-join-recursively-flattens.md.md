---
layout: post
title:  Array#join flattens nested arrays
date:   2024-08-22 19:15:20 -0700
category: til
tags: 
   - join
   - Array
context: ruby
excerpt: "There's no need to explicitly flatten nested arrays before `join`ing."
published: true
---

Suppose you have a nested array like this...

```ruby
[1, [2, 3, [4], 5]]
```

... and you want to convert it into the string `"1, 2, 3, 4, 5"`.

Before I read the documentation for `Array#join`, I would have thought I needed
to `#flatten` the array before I `#join`ed it:

```ruby
[1, [2, 3, [4], 5]].flatten.join(', ') # "1, 2, 3, 4, 5"
```

It turns out `Array#join` recursively calls `Array#join` on nested arrays, so
you don't need to explicitly `#flatten` it. This works:

```ruby
[1, [2, 3, [4], 5]].join(', ') # "1, 2, 3, 4, 5"
```
