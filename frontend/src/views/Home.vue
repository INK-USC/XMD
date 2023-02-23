<template>
  <section id="hero" class="hero d-flex align-items-center" style="width: 100%; height: 60vh; background: #cce5ff; background-size: cover; background-position: center;">
    <div class="container">
      <div class="row">
        <div class="justify-content-center">
          <h1 data-aos="fade-up" style="margin: 0; font-size: 48px; font-weight: 700; color: #361e0b;">XMD: An End-to-End Framework for Interactive Explanation-Based Debugging of NLP Models</h1>
          <h2 data-aos="fade-up" style="color: #444444; margin: 15px 0 0 0; font-size: 26px;" data-aos-delay="400">University of Southern California</h2>
<!--          <h2 data-aos="fade-up" style="color: #444444; margin: 15px 0 0 0; font-size: 26px;" data-aos-delay="400">SONY R&D Center</h2>-->
        </div>
      </div>
    </div>
  </section>
  <section id="overview" class="overview" style="padding:100px; width: 100%;">
      <div class="container" id="app">
        <div class="row">
            <div class="col-md-6">
                    <h2 class="" style="color: #3597d4"> Overview </h2>
                    <p class="text" style="text-align: justify">
                      NLP models are susceptible to learning spurious biases (i.e., bugs) that work on some datasets but do not properly reflect the underlying task. Explanation-based model debugging aims to resolve spurious biases by showing human users explanations of model behavior, asking users to give feedback on the behavior, then using the feedback to update the model.
                      While existing model debugging methods have shown promise, their prototype-level implementations provide limited practical utility.
                    </p>
            </div>
            <div class="col-sm-12 col-xl-6 d-flex text-center" data-aos="zoom-out" data-aos-delay="200">
              <img src="@/assets/overview.png" class="img-fluid" alt="">
            </div>
        </div>

        <div class="row">
            <div class="row" style="margin-top: 25px;">
                <div class="col-xl">
                    <h2 style="color: #3597d4">XMD</h2>
                    <div id="xmd">

                      <div class="card">
                        <div class="card-header" id="setting">
                          <h5 class="mb-0">
                              <button class="btn btn-link" data-toggle="collapse" data-target="#expCollapseOne"
                                      aria-expanded="false" aria-controls="expCollapseOne">
                                  <h4 style="color: #213744">Start Framework (Upload Data > Label Setting > Explanation Generation)</h4>
                              </button>
                          </h5>
                        </div>
                        <div id="expCollapseOne" class="collapse" aria-labelledby="expHeadingOne" data-parent="#xmd">
                          <div class="card-body">
                              <div class="row">
                                  <img src="@/assets/gif/setting.gif" alt="see caption" class="img-fluid" style="width: 100%; margin: 0 auto"/>
                              </div>
                          </div>
                        </div>
                      </div>

                      <div class="card">
                        <div class="card-header" id="instance">
                          <h5 class="mb-0">
                              <button class="btn btn-link" data-toggle="collapse" data-target="#expCollapseTwo"
                                      aria-expanded="false" aria-controls="expCollapseTwo">
                                  <h4 style="color: #213744">Instance Explanation</h4>
                              </button>
                          </h5>
                        </div>
                        <div id="expCollapseTwo" class="collapse" aria-labelledby="expHeadingTwo" data-parent="#xmd">
                          <div class="card-body">
                              <div class="row">
                                  <img src="@/assets/gif/instance.gif" alt="see caption" class="img-fluid" style="width: 100%; margin: 0 auto"/>
                              </div>
                          </div>
                        </div>
                      </div>

                      <div class="card">
                        <div class="card-header" id="task">
                          <h5 class="mb-0">
                              <button class="btn btn-link" data-toggle="collapse" data-target="#expCollapseThree"
                                      aria-expanded="false" aria-controls="expCollapseThree">
                                  <h4 style="color: #213744">Task Explanation</h4>
                              </button>
                          </h5>
                        </div>
                        <div id="expCollapseThree" class="collapse" aria-labelledby="expHeadingThree" data-parent="#xmd">
                          <div class="card-body">
                              <div class="row">
                                  <img src="@/assets/gif/task.gif" alt="see caption" class="img-fluid" style="width: 100%; margin: 0 auto"/>
                              </div>
                          </div>
                        </div>
                      </div>

                    </div>
                </div>
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
