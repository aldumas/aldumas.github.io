---
layout: post
title: Predefined globals
date: 2024-05-03 09:26:16 -0700
category: notes
tags: 
   - ruby
   - globals
   - todo
context: ruby
excerpt: "Predefined global constants and variables."
published: false
---

See https://ruby-doc.org/current/globals_rdoc.html.

# $!

```ruby
def describe(value)
  puts "value is a #{value.class.name}"
  puts "value as a string: '#{value}'"
  puts "value's message: #{value.message}" if value.respond_to? :message
  puts '-' * 20
end

begin
  raise StandardError.new("Hey there, I am an error!")
rescue
  describe $!

  # Output:
  # ======
  #
  # value is a StandardError
  # value as a string: 'Hey there, I am an error!'
  # value's message: Hey there, I am an error!
  # --------------------
end

describe $!

# Output:
# ======
#
# value is a NilClass
# value as a string: ''
# --------------------
```
