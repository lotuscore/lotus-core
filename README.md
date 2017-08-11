# Lotus Core #

### Installations

1. Install OS Dependencies:

    `> sh bootstrap.sh` (not included npm)

2. Install virtualenv + virtualenvwrapper: https://github.com/brainsik/virtualenv-burrito

3. Create virtualenv and install python dependencies

    ```
    mkvirtualenv lotus-core --python="$(which python3)"
    pip install -r requirements.pip
    ```

4. Install testprc

    `npm install -g ethereumjs-testrpc`

### Run Project

1. Run testrpc:

     `> testrpc`

2. Deploy contracts:

     `> python deploy.py`

3. Create `.env` file based on `env.example` and update `TOKEN_CONTRACT_ADDRESS` variable

4. Run app:

     `> ./app.run`