# XMD: An End-to-End Framework for Interactive Explanation-Based Debugging of NLP Models
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-green.svg?style=flat-square)](http://makeapullrequest.com)
[![arXiv](https://img.shields.io/badge/arXiv-2210.16978-b31b1b.svg)](https://arxiv.org/abs/2210.16978)

This repo provides the model, code & data of our paper: [XMD: An End-to-End Framework for Interactive Explanation-Based Debugging of NLP Models](https://arxiv.org/abs/2210.16978).
[[PDF]](https://arxiv.org/pdf/2210.16978.pdf)

## Overview

NLP models are susceptible to learning spurious biases (i.e., bugs) that work on some datasets but do not properly reflect the underlying task. Explanation-based model debugging aims to resolve spurious biases by showing human users explanations of model behavior, asking users to give feedback on the behavior, then using the feedback to update the model. While existing model debugging methods have shown promise, their prototype-level implementations provide limited practical utility.

Project website: [https://inklab.usc.edu/xmd](https://inklab.usc.edu/xmd)

## Getting Started:

- This project is intended to be deployed on modern linux environments.
- Install Python 3, verify install status by using `python3 --version` to check. python may be installed under different aliases, use the appropriate one on your system.

<details>
<summary><b>Setup Environment</b></summary>
<p>

1. Create a virtual environment using:
    - anaconda: 
        1. `conda create -n xmd python=3.8`
    - virtualenv:
        1. `python3 -m pip install virtualenv`
        2. `python3 -m venv xmd`

2. Activate your environment:
    - anaconda: `conda activate hilt-demo`
    - virtualenv: `source hilt-demo/bin/activate`
    
5. Install prerequisites:
    - `pip install -r requirements.txt`
    - Note that requirements.txt may contain package version not compatible with your installation. Please adjust accordingly.
</p>
</details>

<br/>

<details>
<summary><b>Setup Backend</b></summary>
<p>

1. Setup PostgreSQL
   1. [Follow postgres's instruction to install postgres 12 on your local system](https://www.postgresql.org/download/)
   2. Make sure postgres is started and enabled by `sudo systemctl start postgresql-12` and `sudo systemctl enable postgresql-12`
   3. Verify postgres status by running `sudo systemctl status postgresql-12`
   4. Create a postgrees user by running `sudo -u postgres createuser hilt-user`
   5. Modify `/var/lib/pgsql/12/data/pg_hba.conf` so that the identification method use md5. [See here in detail](https://stackoverflow.com/questions/50085286/postgresql-fatal-ident-authentication-failed-for-user) You can use any text editor you want. I would recommend `micro` or `nano`. As a backup,`vi` should be installed by default on any modern linux systems.
   6. Open `annotation_backend/create_empty_db.sql`, you will need to execute these sql commands as the postgres user. This can be done by:
       1. `cat annotation_backend/create_empty_db.sql` to print the command to the current console.
       2. `sudo -u postgres psql` to switch to postgres user and enter the postgres environment. If prompt for password, enter one you configured during the setup process. Try 123.
       3. Copy and paste commands in `annotation_backend/create_empty_db.sql` into the command window to execute these sql commands to initialize and configure the database.
       4. Exit postgres environment  by typing `\q`

2. Setup Django   
   1. Use `python3 annotation_backend/manage.py migrate` to setup postgres database for access
   2. Use `python annotation_backend/manage.py createsuperuser` to setup django super user for website login
    
3. Start the backend by using `python annotation_backend/manage.py runserver 0.0.0.0:8000` Note 8000 here is hard coded in, you need to move other services that may be running on 8000 before hand.
4. After verifying that the backend can be access via a web browser and can be accessed normally, it is recommended to use systemd or tmux to start a headless instance to allow server to serve after logout of current instance.
5. It is recommended to use `chmod` and `chown` to set appropriate  permissions for the database and source code files. Note that postgresql db need to be accessed as the postgres user.
    
(Old) Follow Django annotation backend installation instructions [here](annotation_backend/README.md)

</p>
</details>
<br/>
<details>
<summary><b>Setup Frontend</b></summary>
<p>
    
- Follow Vue.js frontend installation instructions [here](frontend/README.md)

</p>
</details>
<br/>

<details>
<summary><b>Directory overview</b></summary>
<p>

- `annotation_backend/`
    - `annotation_backend/` - django application
    - `hilt_annotation/` - django application
    - `sample_data/` - sample datasets for testing
- `frontend/` - Vue.js frontend project directory

</p>
</details>
<br/>

## Citation
If you find our work helpful, please cite the following:
```bib
@article{lee2022xmd,
  title={XMD: An End-to-End Framework for Interactive Explanation-Based Debugging of NLP Models},
  author={Lee, Dong-Ho and Kadakia, Akshen and Joshi, Brihi and Chan, Aaron and Liu, Ziyi and Narahari, Kiran and Shibuya, Takashi and Mitani, Ryosuke and Sekiya, Toshiyuki and Pujara, Jay and Ren, Xiang},
  journal={arXiv preprint arXiv:2210.16978},
  year={2022}
}
```