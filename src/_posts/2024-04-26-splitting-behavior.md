---
layout: post
title:  String#split behavior
date:   2024-04-26 14:07:00 -0700
category: til
tags: 
   - ruby
   - corner-case
   - String
   - split
excerpt: "When to expect empty arrays and empty strings in the output."
published: true
---

## Standard case

```ruby
'x:y'.split(':') # => ['x', 'y']
```

## Corner cases

```ruby
''.split(':')     # => []
':'.split(':')    # => []
'x'.split(':')    # => ['x']
'x:'.split(':')   # => ['x']
':x'.split(':')   # => ['', 'x']
'::'.split(':')   # => []
'x::y'.split(':') # => ['x', '', 'y']
'::x'.split(':')  # => ['', '', 'x']
'x::'.split(':')  # => ['x']
```

## Takeaways

For the following discussion, a "segment" is defined as the (possibly empty) string between separators or at the start
or end of the string.

1. The result is always an array.
2. The only time an empty string will appear in the resulting array is when one or more empty segments are followed by a
   non-empty segment. Some notable implications:
   <ol class="list-alpha">
      <li>A trailing separator will <strong>not</strong> produce an empty string in the result.</li>
      <li>If all the segments in the string are empty, the resulting array will <em>always</em> be empty.</li>
   </ol>
