---
layout: post
title:  The Body HTML Element and its Margins
date:   2024-05-14 12:16:20 -0700
category: til
tags: 
   - css
   - corner-case
context: css
excerpt: "The background shows through the margins."
published: true
---

Usually, the background of an HTML element only fills the content area of the element, not the margins. If you set a background color on a `p` element and give it a `margin-left` of `10px`, that margin remains the color of its parent element, not the backgound color of the paragraph.

**This is not the case for the `body` element.**

Since the `body` element represents the content of the entire page, its margin has a little different meaning. If you set a background color on the `body` element and give it a margin, the color of the margin is that color.

A way to think of it is that the margin of the `body` element is not about positioning the body element relative to other elements (since it is already the top level element) but about setting a document-level margin for its child elements.
