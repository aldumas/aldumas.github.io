---
layout: post
title:  "String#split behavior"
date:   2024-04-26 14:07:00 -0700
categories: til
tags: ruby corner-case String split
published: true
---

## Standard case

```ruby
'x:y'.split(':') # => ['x', 'y']
```

## Corner cases

```ruby
''.split(':') # => []
':'.split(':') # => []
'x'.split(':') # => ['x']
'x:'.split(':') # => ['x']
':x'.split(':') # => ['', 'x']
'::'.split(':') # => []
'x::y'.split(':') # => ['x', '', 'y']
'::x'.split(':') # => ['', '', 'x']
```

## Takeaways

For the following discussion, a "segment" is defined as the (possibly empty) string between separators or at the start
or end of the string.

1. The result is always an array.
2. The only time an empty string will appear in the resulting array is when one or more empty segments are followed by a
   non-empty segment. Some notable implications:
   1. A trailing separator will **not** produce an empty string in the result.
   2. If all the segments in the string are empty, the resulting array will *always* be empty.
