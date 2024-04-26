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

# Splitting by an empty string

'x y'.split('') # => ['x', ' ', 'y']
''.split('') # => []
```

## Takeaways

1. The result is always an array.
2. The only time an empty string will appear in the resulting array is when the string *begins* with the separator. A
   trailing separator will **not** produce an empty string in the result.
3. If there's no content in the string (i.e. no non-separator characters), the resulting array will always be empty.
   Conversely, if there is any content in the string, the resulting array will never be empty.
4. Splitting by an empty string splits into individual characters.
   
