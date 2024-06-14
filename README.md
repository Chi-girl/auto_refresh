#### Setting up Virtual Environment

1. Open CMD
2. Run "pip install virtualenv"
3. Change directory to the project's folder "cd <path-to-project>"
4. Creating the virtual environment, Run "virtualenv venv"

#### Running the project

1. Activating the virtual environment, Run "venv/Scripts/activate" (note: include the quotation marks)
2. Installing the required packages, Run "pip install -r requirements.txt
3. Running the app, Run "python src/main.py"

#### Build

1. Run "python build.py"
2. Locate the application in the "dist/" folder


Steps for Modifications:
Steps:
1. process.py :: Logic
2. main.py :: "in a case of added functions: add it in the dictionary"
3. interface.py
	- Button lambda: app.run_action("dict_key_from_func_main.py")



For packaging: 
1. run python build.py