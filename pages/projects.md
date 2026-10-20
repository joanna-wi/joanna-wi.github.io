---
layout: page
title: Projects
permalink: /projects/
---

<div class="tabs">
  <input type="radio" name="tab" id="tab1" checked>
  <input type="radio" name="tab" id="tab2">

  <div class="tab-labels">
    <label for="tab1">Project one</label>
    <label for="tab2">Project two</label>
  </div>

  <section class="tab-panel" id="panel1">
    <img src="{{ site.baseurl }}/assets/img/project1.jpg" alt="project one header">
    <p>short description of project one.</p>
    <ul>
      <li><a href="https://github.com/USERNAME/REPO/tree/main/project1-folder">project folder</a></li>
      <li><a href="https://github.com/USERNAME/REPO/blob/main/project1-folder/analysis.py">analysis script</a></li>
    </ul>
  </section>

  <section class="tab-panel" id="panel2">
    <img src="{{ site.baseurl }}/assets/img/project2.jpg" alt="project two header">
    <p>short description of project two.</p>
    <ul>
      <li><a href="https://github.com/USERNAME/REPO/tree/main/project2-folder">project folder</a></li>
    </ul>
  </section>
</div>
