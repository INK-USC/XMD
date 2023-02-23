<template>
  <section id="hero" class="hero d-flex align-items-center" style="width: 100%; height: 60vh; background: #cce5ff; background-size: cover; background-position: center;">
    <div class="container">
      <div class="row">
        <div class="justify-content-center">
          <h1 data-aos="fade-up" style="margin: 0; font-size: 48px; font-weight: 700; color: #361e0b;">XMD: An End-to-End Framework for Interactive Explanation-Based Debugging of NLP Models</h1>
          <h2 data-aos="fade-up" style="color: #444444; margin: 15px 0 0 0; font-size: 26px;" data-aos-delay="400">University of Southern California</h2>
          <h2 data-aos="fade-up" style="color: #444444; margin: 15px 0 0 0; font-size: 26px;" data-aos-delay="400">SONY R&D Center</h2>
        </div>
      </div>
      <div class="row">
          <div class="col-md-6">
            <br><br>
              <p class="text" style="text-align: justify">
                NLP models are susceptible to learning spurious biases (i.e., bugs) that work on some datasets but do not properly reflect the underlying task. Explanation-based model debugging aims to resolve spurious biases by showing human users explanations of model behavior, asking users to give feedback on the behavior, then using the feedback to update the model.
                While existing model debugging methods have shown promise, their prototype-level implementations provide limited practical utility.
              </p>
          </div>
      </div>
    </div>
  </section>
</template>


<script>
// @ is an alias to /src

// home page
export default {
  name: "HomePage",
  components: {
  },
};
</script>
