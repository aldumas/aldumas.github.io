---
layout: default
---

Personal writing from one family's life with Phelan-McDermid Syndrome: the
ordinary days, the paperwork, the people around our daughter, and getting
ready for the years after us.

## Recent posts

<% if collections.posts.resources.empty? %>
Nothing published yet.
<% else %>
<ul>
  <% collections.posts.resources.first(10).each do |post| %>
    <li>
      <a href="<%= post.relative_url %>"><%= post.data.title %></a>
      <small><%= post.date.strftime("%B %-d, %Y") %></small>
    </li>
  <% end %>
</ul>
<% end %>
