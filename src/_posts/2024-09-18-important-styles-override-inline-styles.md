---
layout: post
title:  Important styles override inline styles
date:   2024-09-18 09:17:00 -0700
category: til
tags: 
   - css
   - important
   - cascade
context: css
excerpt: "`!important` styles are considered to be from a higher-priority origin than author styles"
published: false
---

Consider this code:

```html
<style>
  h1 {
    color: green !important;
  }
</style>

<h1 style="color: blue;">This text is green</h1>
```

The color of the text will be green based on the cascade. When determining the
final value of a property, the cascade looks at the following, in order:

1. Origin
1. Specificity
1. Source order

Because the `!important` color rule is considered to be from a higher-priority
origin than the inline style, specificity and source order do not apply.

If you want to make sure an inline style takes precedence over any `!important`
styles, you can mark the inline style as `!important`:

```html
<style>
  h1 {
    color: green !important;
  }
</style>

<h1 style="color: blue !important;">This text is blue</h1>
```
