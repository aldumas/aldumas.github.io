---
layout: post
title: Inline rescue
date: 2024-05-03 19:02:39 -0700
category: til
tags: 
   - ruby
   - language
   - rescue
context: ruby
excerpt: "For when you don't care about the error type and just want to convert it to some value."
published: false
---

```ruby
require 'http'

urls = ['https://github.com', 'https://doesnotexist']

pages = urls.map { |url| HTTP.get(url) rescue nil }.compact
  

#puts pages

# This is equivalent to:

pages = urls.map do |url| 
  HTTP.get(url)
rescue
  nil
end.compact

puts pages

# pages = urls.map do |url|
#   page = HTTP.get(url)
#   { url:, page: }
# # rescue
# #   { url:, page: ''}
# end

# puts pages


# One shortcoming is that you cannot specify the type of errors you intend to rescue.
```