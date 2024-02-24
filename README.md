# Deeplogic Assignment

## Task 1 
- script for fetching data from picture or pdf is inside `script` folder.


## Task 2
- Web application is developed using Django and celery

## Requirement

- Python 3.X and virtual environment package
- redis ( for message broker )
- Web browser

---

## How to run Locally

1. make a directory and go to the directory
2. make a virtual environment <br>
   <b>a.</b> for windows
   ```bash
     python -m venv dev-env
   ```
   <b>b.</b> for unix & linux system
   ```bash
     python3 -m venv dev-env
   ```
3. Create the directory and inside the directory clone the project.
   ```bash
     git clone https://github.com/AbhiMisRaw/deeplogic-assignment
   ```
4. Enable virtual environment<br>
   <b>a.</b> for windows
   ```bash
     dev-env\Scripts\activate
   ```
   <b>b.</b> for unix & linux system
   ```bash
     source dev-env/bin/activate
   ```
5. Go to the cloned project directory
   ```bash
     cd dataExtractor
   ```
6. Install dependencies

   ```bash
     pip install -r requirements.txt
   ```
7. Run migrations
   ```bash
     python manage.py makemigrations
     python manage.py migrate
   ```
8.  Start the server
    ```bash
      python manage.py runserver
    ```
