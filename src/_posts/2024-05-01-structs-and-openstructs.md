---
layout: post
title: Structs and OpenStructs
date: 2024-05-01 12:48:40 -0700
category: til
tags: 
   - ruby
   - struct
   - openstruct
   - hash
context: ruby
excerpt: "Using Structs and OpenStructs for value-oriented data."
published: true
---

Sometimes you have a set of related data that you want to travel together, e.g.
as Data Transfer Objects (DTOs). In these cases, a class might not be necessary,
and perhaps inconvenient if you want to be able to compare these objects using
value-semantics, since classes by default compare references.

You could use `Hash`es to side-step this, but they can be inconvenient for
another reason: accessing the members is syntactically different than invoking
methods. If you want to support method-call syntax AND use value-semantics, you
can use a `Struct` or `OpenStruct`.

# Struct

```ruby
Food = Struct.new(:name, :price, :has_gluten)

menu = [
  Food.new("Spaghetti Simpatico", "$12.00", true),
  Food.new("Beef Tonight", "$19.00", false),
  Food.new("Pizza ala Cauliflower", "$15.00", false)
]

# output gluten-free menu
puts menu.reject(&:has_gluten)
```

You can use keyword arguments instead if you define the `Struct` with `keyword_init` set to `true`.

```ruby
Food = Struct.new(:name, :price, :has_gluten, keyword_init: true)

menu = [
  Food.new(name: "Spaghetti Simpatico", price: "$12.00", has_gluten: true),
  Food.new(name: "Beef Tonight", price: "$19.00", has_gluten: false),
  Food.new(name: "Pizza ala Cauliflower", price: "$15.00", has_gluten: false)
]

# output gluten-free menu
puts menu.reject(&:has_gluten)
```

If you want to define other methods in the `Struct`, you can do that, too.

```ruby
Food = Struct.new(:name, :price, :has_gluten, keyword_init: true) do
  alias :gluten? :has_gluten

  def menu_entry
    "#{name} ... #{price}#{gluten? ? '' : ' (GF)'}"
  end
end

menu = [
  Food.new(name: "Spaghetti Simpatico", price: "$12.00", has_gluten: true),
  Food.new(name: "Beef Tonight", price: "$19.00", has_gluten: false),
  Food.new(name: "Pizza ala Cauliflower", price: "$15.00", has_gluten: false)
]

# output list of formatted menu items
puts menu.map(&:menu_entry)
```

Here, I used `alias` and a regular `def` to define methods. It's good to ask
yourself if you actually need a class if you find yourself defining methods on a
`Struct`. Using `alias` is probably OK, but adding actual behavior might mean
you are using the object as more than a DTO.

# OpenStruct

You might have a `Hash` object which you want to access using method-call
syntax. One way you could do this is with a `Struct`.

```ruby
hash = { name: 'Spaghetti Simpatico', price: '$12.00', has_gluten: true }

# define the struct
Food = Struct.new(*hash.keys, keyword_init: true)

# create the instance
object = Food.new(**hash)

# use the instance
puts object.name
```

This is cumbersome, though, since you have to define the struct, then create the
instance. An easier method is to use `OpenStruct`.

```ruby
require 'ostruct'

hash = { name: 'Spaghetti Simpatico', price: '$12.00', has_gluten: true }

# define the struct
object = OpenStruct.new(hash)

# use the instance
puts object.name
```

It's not as convenient to define methods on these since each call creates a new
class. If you just have a single instance you are working with you can define a
singleton method on the instance.

If, however, you have several instances, you can subclass `OpenStruct` and
define the method there, but if you're defining a class for this reason, you
might as well not use `OpenStruct` at all and just define a class or use a
regular `Struct`.

When using `OpenStruct`, be sure to read through the
[caveats](https://rubydoc.info/stdlib/ostruct/OpenStruct).

Lastly, see the mindmap at the end of the
[RubyGuide on using Struct and OpenStruct](https://www.rubyguides.com/2017/06/ruby-struct-and-openstruct/).
It's helpful to see the differences between classes vs `Struct`s vs
`OpenStruct`s and can help you figure out which one to use for your use case.
