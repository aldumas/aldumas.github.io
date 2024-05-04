---
layout: post
title: Key ideas from Confident Ruby by Avdi Grimm
date: 2024-05-02 19:29:37 -0700
category: notes
tags: 
   - ruby
   - oop
   - design
   - method
context: ruby
excerpt: "Key ideas about method design."
published: false
---

The subject of this book is the design of methods.

# Categories

Every line of code in a method can be categories according to these types:

1. Collecting input
2. Performing work
3. Delivering output
4. Handling failures

Avdi also identifies 2 other types which are less common:

5. diagnostics
6. cleanup

# Telling a clear story

You want the method to tell a clear story.

In order to tell a clear story, we need to be able to trust that the objects
we send messages to will understand and respond to those messages. To be able to
do that, we need to:

1. figure out what messages we need to be sent to perform the work of the method
2. determine which roles correspond to those messages
3. ensure the method receives objects which will serve in those roles

In order to write a method that tells a clear story, you need to be aware of the
"MacGuyver" method; that is, a method design that is overly influenced on the
objects which happen to be available in the environment of the method. Instead,
in an input collection stanza, map the value provided from the environment into
an object which can serve in the needed role, and tell the story in terms of the
roles and messages sent to those roles you identified.

# Collecting input

Carefully thinking about the inputs your method needs can have a
disproportionately large effect on the clarity of the method.

In thinking through this, you need to consider:

- what inputs are needed and how they should be delivered
- how lenient to be in accepting many types of input
- whether to adapt the method's logic to work with the received object types or
  the converse

