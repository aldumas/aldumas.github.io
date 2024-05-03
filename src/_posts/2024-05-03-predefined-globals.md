---
layout: post
title: Predefined global `$!`
date: 2024-05-03 09:26:16 -0700
category: til
tags: 
   - ruby
   - globals
context: ruby
excerpt: "It holds the last error raised."
published: true
---

`$!` refers to the last error raised.

```ruby
begin
  raise StandardError.new("Hey there, I am an error!")
rescue
  puts "$! is a #{$!.class.name}"
end

puts "$! is a #{$!.class.name}"
```

Notice that `$!` becomes `nil` after the `rescue` clause completes.

In this case, it's clearer to declare a variable:

```ruby
begin
  # ...
rescue => e
  # ...
end
```

The one use case I am aware of for `$!` is converting an exception to a value
using inline-rescue.

```ruby
value_or_error = {}.fetch(:name) rescue $!
puts value_or_error.class.name # => KeyError
```

This allows you to succinctly capture the exception for logging or processing
some other way without cluttering up your method with `begin` and `rescue`
blocks. See [this <span class="small-caps">graceful.dev</span> video](https://graceful.dev/courses/the-freebies/modules/ruby-language/topic/episode-022-inline-rescue/)
for more information.

See also [the list of predefined globals](https://ruby-doc.org/current/globals_rdoc.html).
