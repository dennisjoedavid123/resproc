# resproc
============
Getting Started
---------------

- Change directory into your newly created project.

    cd resproc

- Create Input and Output Folders
   mkdir input ouput

- Create a Python virtual environment.

    python3 -m venv env

- Enter into the Virtual Environment

    source env/bin/activate


- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Go into the ripper.py [ Its a crappy way I know ]
  
  Change INPUT_FOLDER to point to the folder where the input files are present

- cd into src folder 

    python ripper.py 

- Output folder will have a output.csv file. 

    Rename the output.csv to another file name in case you need a different folder 
    to run.