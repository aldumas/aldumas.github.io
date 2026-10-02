---
layout: page
title: Posts
---

<% if collections.posts.resources.empty? %>
Nothing published yet.
<% else %>
<ul>
  <% collections.posts.resources.each do |post| %>
    <li>
      <a href="<%= post.relative_url %>"><%= post.data.title %></a>
      <small><%= post.date.strftime("%B %-d, %Y") %></small>
    </li>
  <% end %>
</ul>
<% end %>
