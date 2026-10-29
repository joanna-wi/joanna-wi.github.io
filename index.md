---
layout: page
permalink: /
---

<section id="home">
<div class="home">
  <img class="profile-photo" src="{{ site.baseurl }}/assets/img/profile-img-color.jpg" alt="my photo">
  <div class="home-text">
    <h1>Hi, I'm Joanna!</h1>
    <p style="text-align: center;">I help bring companies closer to their clients by tapping into the science of the human mind and behaviour. You can count on me to foster open conversations where people's needs are heard, incorporate novel devices and technologies to discover what they cannot express, and connect it all back to your goal with insights that make decisions easier.<br><br>See examples of my work in <strong style="color:#90b4e1;">Projects</strong> and find out more about my experience in <strong style="color:#90b4e1;">CV</strong>.</p>
  </div>
</div>
</section>



<section id="projects">
  <h2>Projects</h2>
<div class="project-list">
{% for project in site.projects %}
  <a class="project-card" href="{{ site.baseurl }}{{ project.url }}">
    <img src="{{ site.baseurl }}/assets/img/{{ project.image }}" alt="">
    <h2>{{ project.title }}</h2>
    <p>{{ project.description }}</p>
  </a>
{% endfor %}
</div>
</section>



<section id="cv">
  <h2>CV</h2>
<a href="{{ site.baseurl }}/assets/img/Joanna%20Wilkosz%20-%20CV.pdf" target="_blank" rel="noopener noreferrer">View my CV (.pdf)</a>

<div style="height:3rem;"></div>

<h2 style="font-size:2rem; margin:0 0 1.5rem; padding-bottom:.5rem; border-bottom:1px solid #d1d1d1;">Areas where I can contribute</h2>

<style>
.cv-box { border:.5px solid #444; border-radius:3px; margin:1rem 0; background:#000; }
.cv-box summary { list-style:none; cursor:pointer; padding:1.25rem 3.5rem 1.25rem 2.5rem; position:relative; display:flex; flex-direction:column; justify-content:center; min-height:6rem; }
.cv-box summary::-webkit-details-marker { display:none; }
.cv-box summary::after { content:"\25BE"; position:absolute; right:1.5rem; top:50%; transform:translateY(-50%); font-size:1.5rem; transition:transform .2s; }
.cv-box[open] summary::after { transform:translateY(-50%) rotate(180deg); }
.cv-box[open] .cv-short { display:none; }
.cv-box h3 { margin:0 0 .5rem; line-height:1.3; }
.cv-box h3 { color:#90b4e1; }
.cv-box ul { margin:0; padding:0 0 0 1.25rem; list-style-position:outside; }
.cv-box li { margin-left:0; padding-left:0; }
.cv-short li { font-weight:bold; margin:0; line-height:1.5; }
.cv-box[open] summary { min-height:0; padding-bottom:.75rem; }
.cv-box[open] h3 { margin-bottom:0; }
.cv-full { padding:0 3.5rem 1.25rem 2.5rem; }
.cv-full li { margin:0 0 1.5rem; text-align:justify; }
.cv-full li:last-child { margin-bottom:0; }
.cv-full li { font-size:1rem; line-height:1.75; }
.cv-full li br { display:none; }
.cv-full strong { display:block; margin-bottom:.5rem; }
</style>

<details class="cv-box">
  <summary>
    <h3>End-to-end project delivery</h3>
    <ul class="cv-short">
      <li>Consumer &amp; market research</li>
      <li>Coordination of multidisciplinary assignments</li>
      <li>Protocols &amp; record-keeping</li>
    </ul>
  </summary>
  <div class="cv-full">
    <ul>
      <li><strong>Consumer &amp; market research</strong><br>Through scientific consulting work, I have gained experience in conducting consumer preference studies spanning a wide range of industries (FMCG, wellness, toy, automotive, advertising, pharmaceutical), geographical markets, and methods. I am keen to continue helping businesses optimise their customer journey across in-person, digital, and offline touchpoints.</li>
      <li><strong>Coordination of multidisciplinary assignments</strong><br>From design and piloting to data collection, analysis, and reporting, I have taken responsibility for delivering outcomes of each project stage against deadlines and targets. I thrive in roles situated at the intersection of several domains, where I can contribute to team success with a collaborative, solution-oriented attitude.</li>
      <li><strong>Protocols &amp; record-keeping</strong><br>Protocol development, record maintenance, and responsible handling of sensitive information are my strong suits. I am always glad to assume ownership of procedure standardisation and workflow refinement.</li>
    </ul>
  </div>
</details>

<details class="cv-box">
  <summary>
    <h3>Insights &amp; analytics</h3>
    <ul class="cv-short">
      <li>Mixed-method analysis</li>
      <li>Business-oriented recommendations</li>
      <li>Visual storytelling</li>
    </ul>
  </summary>
  <div class="cv-full">
    <ul>
      <li><strong>Mixed-method analysis</strong><br>I am well-versed in analysing qualitative and quantitative data (sociodemographic, behavioural, physiological, business performance measures) with the use of digital tools such as Excel, Jamovi, and Python. My university education and research work have helped me develop a sound understanding of statistical methods along with an ability to extract meaningful patterns by synthesising information from multiple sources.</li>
      <li><strong>Business-oriented recommendations</strong><br>With complex technical findings as raw material, I find joy in translating the science into narratives suitable for informing product strategy, innovation, and consumer experience improvements. Having worked with both academic and commercial clients, I prioritise tailoring insights to each audience’s goals and level of expertise.</li>
      <li><strong>Visual storytelling</strong><br>Over the years, I have built a strong foundation in presenting data compellingly by combining visuals with commentary in PowerPoint reports, Power BI dashboards, and infographics.</li>
    </ul>
  </div>
</details>

<details class="cv-box">
  <summary>
    <h3>Stakeholder engagement &amp; relationship management</h3>
    <ul class="cv-short">
      <li>Data collection</li>
      <li>Presale activities</li>
      <li>Customer support</li>
    </ul>
  </summary>
  <div class="cv-full">
    <ul>
      <li><strong>Data collection</strong><br>I firmly believe that meeting people face to face yields the deepest insight, which is why I treasure every chance to connect with consumers and patients during data collection. I can lead sessions with professionalism and ease, while creating a welcoming atmosphere where every participant is fully informed and well cared for.</li>
      <li><strong>Presale activities</strong><br>Building on a five-month SaaS sales programme, I am ready to deliver product demonstrations focused on understanding prospects’ technical needs, identifying optimal solutions, and opening the door to upsell opportunities.</li>
      <li><strong>Customer support</strong><br>In my last role, I handled client and prospect conversations via Intercom, developing experience in answering inquiries, troubleshooting technical problems, and providing onboarding assistance.</li>
    </ul>
  </div>
</details>

<details class="cv-box">
  <summary>
    <h3>Knowledge sharing</h3>
    <ul class="cv-short">
      <li>Presentations &amp; workshops</li>
      <li>Team enablement</li>
      <li>Marketing content preparation</li>
    </ul>
  </summary>
  <div class="cv-full">
    <ul>
      <li><strong>Presentations &amp; workshops</strong><br>Results, proposal, and literature review presentations for technical and non-technical audiences at different levels of seniority have been a continuous part of my work, strengthening the clarity with which I can communicate ideas. I am also open to leading external workshops or trainings.</li>
      <li><strong>Team enablement</strong><br>Beyond client-facing work, I have experience in delivering regular internal updates aimed at supporting team learning and product improvements. Similarly, I am enthusiastic about contributing to the training and mentoring of junior colleagues.</li>
      <li><strong>Marketing content preparation</strong><br>Crafting customer success stories and sample reports has given me practice in turning complex technical concepts into accessible and engaging materials geared towards generating product interest as well as increasing brand trust.</li>
    </ul>
  </div>
</details>

<details class="cv-box">
  <summary>
    <h3>Scientific &amp; technical expertise</h3>
    <ul class="cv-short">
      <li>Neuroscience, psychology, psychiatry</li>
      <li>Human biology</li>
      <li>Biosensors and medical devices</li>
    </ul>
  </summary>
  <div class="cv-full">
    <ul>
      <li><strong>Neuroscience, psychology, psychiatry</strong><br>With a BSc in Neurobiology and an MSc in Neuroscience, I bring extensive knowledge of brain function, along with a proficiency at grounding project design and findings in scholarly research. No matter the task, at the core of my work lies a passion for uncovering the drivers behind people's behaviours, attitudes, and choices.</li>
      <li><strong>Human biology</strong><br>My education and professional background extend beyond the specialisation in the nervous system to a holistic understanding of anatomy and physiology. This includes hands-on experience in analysing muscle movements and autonomic signals.</li>
      <li><strong>Biosensors and medical devices</strong><br>I have worked with a broad spectrum of hardware and software tools across consulting (eye tracking, facial expression analysis, voice analysis, EDA, EMG, ECG, respiration, EEG, fNIRS), clinical work (EEG, EMG), and entrepreneurship research (fMRI), gaining theoretical and practical command of their functioning, alongside the capacity to master new technologies quickly.</li>
    </ul>
  </div>
</details>

<script>
document.querySelectorAll('.cv-full li').forEach(function (li) {
  li.innerHTML = li.innerHTML.replace(/(^|[\s>])(I|a|A|an|An)\s+(?=\S)/g, '$1$2&nbsp;');
});
</script>
</section>



<section id="contact">
  <h2>Contact</h2>
<style>
.page__content .fa,
table .fa { color:#90b4e1; }
</style>

<table style="border:none; border-collapse:collapse; width:auto; background:none;">
  <tr style="border:none; background:none;">
    <td style="border:none; background:none; width:2.5rem; text-align:center; padding:.5rem 0;"><i class="fa fa-envelope" aria-hidden="true"></i></td>
    <td style="border:none; background:none; padding:.5rem 0;">contact.joannawilkosz@gmail.com</td>
  </tr>
  <tr style="border:none; background:none;">
    <td style="border:none; background:none; width:2.5rem; text-align:center; padding:.5rem 0;"><i class="fa fa-phone" aria-hidden="true"></i></td>
    <td style="border:none; background:none; padding:.5rem 0;">+45 50 19 01 12</td>
  </tr>
  <tr style="border:none; background:none;">
    <td style="border:none; background:none; width:2.5rem; text-align:center; padding:.5rem 0;"><i class="fa fa-linkedin" aria-hidden="true"></i></td>
    <td style="border:none; background:none; padding:.5rem 0;"><a href="https://www.linkedin.com/in/profile-joanna-wilkosz" target="_blank">linkedin.com/in/profile-joanna-wilkosz</a></td>
  </tr>
  <tr style="border:none; background:none;">
    <td style="border:none; background:none; width:2.5rem; text-align:center; padding:.5rem 0;"><i class="fa fa-home" aria-hidden="true"></i></td>
    <td style="border:none; background:none; padding:.5rem 0;">2600 Glostrup</td>
  </tr>
</table>
</section>



<script>
(function () {
  var sections = document.querySelectorAll('section[id]');
  function show() {
    var id = location.hash.substring(1) || 'home';
    if (!document.getElementById(id)) id = 'home';
    sections.forEach(function (s) { s.classList.toggle('active', s.id === id); });
    window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', show);
  show();
})();
</script>
