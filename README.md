# HILT-DEMO

TODO: Add project details

---

# Getting Started:

- Install Python 3.8. For detailed environment setup follow `Setup Environment` step.

<details>
<summary><b>Setup Environment</b></summary>
<p>
Note: All paths are relative to being just outside the `HILT-DEMO` directory. Please adjust paths accordingly.

1. Please install Python3.8 (if you use `conda` you can ignore this step and setup accordingly)
2. Open a new terminal window after installing the above
3. Clone this repo: `git clone https://github.com/danny911kr/HILT-demo.git`
4. Create a virtual environment using:
    - anaconda: `conda create -n hilt-demo python=3.8`
    - virtualenv:
        1. `python3.8 -m pip install virtualenv`
        2. `python3.8 -m venv hilt-demo`

5. Activate your environment:

    - anaconda: `conda activate hilt-demo`
    - virtualenv: `source hilt-demo/bin/activate`

</p>
  </details>
  <br/>

<details>
<summary><b>Setup Frontend</b></summary>
<p>

- Follow Django annotation backend installation instructions [here](annotation_backend/README.md)
- Follow Vue.js frontend installation instructions [here](frontend/README.md)

</p>
</details>
<br/>

<details>
<summary><b>Potential Errors</b></summary>
<p>

- Wrong version of python is being used.
    - To check: if you're getting installation errors, it could be that your machine is running the wrong version of
      python and/or installed packages. To check run `which python` and make sure the returned folder is the path to
      the `leanlife` virtual environment folder. To check that python is looking in the right places check this
      example [here](https://bic-berkeley.github.io/psych-214-fall-2016/sys_path.html#python-looks-for-modules-in-sys-path)
      . Again the path should be the site-packages folder in your `leanlife` virtual environment
    - To Fix: Re-create virtual environment: - `deactivate leanlife` - `rm -rf leanlife` - make sure no other
      virtualenvs are running - open up terminal/command prompt and see if there are paranthesis at the start of each
      line, ex: `(base) user@...` - if this is the case deactivate that environment: `deactivate environment-name`, in
      the above example it would be `deactivate base` - Go to step 4 of installation instructions

</p>
</details>
<br/>

<details>
<summary><b>Directory overview</b></summary>
<p>

- `annotation_backend/`
    - `annotation_backend/` - django application
    - `dist` - vue static files
    - `hilt_annotation/` - django application
    - `sample_data/` - sample datasets for testing
- `frontend/` - Vue.js frontend project directory

</p>
</details>
<br/>
