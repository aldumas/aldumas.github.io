---
layout: page
title: Posts
paginate:
  collection: posts
---

<ul>
  {% for post in paginator.resources %}
    <li>
      <a href="{{ post.relative_url }}">{{ post.data.title }}</a>
    </li>
  {% endfor %}
</ul>

<br />

{% if paginator.total_pages > 1 %}
    {% if paginator.previous_page %}
<a href="{{ paginator.previous_page_path }}"><< Newer posts</a>
    {% endif %}
    {% if paginator.next_page %}
<a href="{{ paginator.next_page_path }}">Older posts >></a>
    {% endif %}
{% endif %}
