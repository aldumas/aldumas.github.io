---
layout: post
title: Inline rescue
date: 2024-05-06 15:03:39 -0700
category: til
tags: 
   - ruby
   - language
   - rescue
context: ruby
excerpt: "For when you don't care about the error type and just want to convert it to some value."
published: true
---

In Ruby, `rescue` can appear in multiple places:

- `begin/rescue` blocks:

```ruby
begin
  # code
rescue
  # code
end
```

- `def/rescue`

```ruby
def perform_work
  # code
rescue
  # code
end
```

- block `rescue`

```ruby
3.times do |attempt|
  # code
rescue
  # code
end
```

I recently learned about a fourth place `rescue` may be used:

- inline `rescue`

```ruby
risky_method rescue "a value"
```

Here's an example. I have a list of URLs that I want to grab the HTML for. If there are any errors, I don't need to know about it. I am OK with just not having that data.

```ruby
require 'http'

urls = ['https://github.com', 'https://doesnotexist']

pages = urls.map { |url| HTTP.get(url) rescue nil }.compact
```

Now `pages` contains a list of HTML strings for all the pages I was able to retrieve. The `rescue nil` part captures any `StandardError` exceptions and returns `nil`. You can return any object you want. In this case, it was convenient to return `nil` so the subsequent `compact` could remove it from the final array.

The above code is equivalent to:

```ruby
pages = urls.map do |url| 
  HTTP.get(url)
rescue
  nil
end.compact
```

One of the caveats of using inline-rescue is that it swallows a very general exception, and there may be some exceptions, either now or with future code changes, which you might want to handle or allow to propagate instead of returning the value.
