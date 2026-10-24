---
layout: page
title: Projects
permalink: /projects/
---
<br>

<div class="project-list">
{% for project in site.projects %}
  <a class="project-card" href="{{ site.baseurl }}{{ project.url }}">
    <img src="{{ site.baseurl }}/assets/img/{{ project.image }}" alt="">
    <h2>{{ project.title }}</h2>
    <p>{{ project.description }}</p>
  </a>
{% endfor %}
</div>
