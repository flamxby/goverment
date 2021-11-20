# Instructions How to Install and Run Locally
## Prerequisite (required) software
|    Name of software    | Versions |
|:----------------------:|:--------:|
|Python|Using at least version 3.7 or higher|

* **Python** is a programming language that lets you work more quickly and integrate your systems more effectively.

### How to Check Python Version 
> To check the version installed, open a terminal window and entering the following:
* Linux/MacOS:
    ```
    $ python3 –-version
    ``` 
* Windows: 
    ``` 
    ...\> python ––version
    ```

## How to clone [government](https://github.com/flamxby/government) project
* Access to a command-line/terminal window.
    * Linux:
        ```
        CTRL-ALT-T or CTRL-ALT-F2
        ``` 
    * Windows: 
        ``` 
        WIN+R > type powershell > Enter/OK or Type in search tap "cmd"
        ```
    * MacOS: 
        ```
        Finder > Applications > Utilities > Terminal
        ```
* Change directory to the directory that the user wants to run the application.
    ```
    cmd> cd directory name
    ```
* Use git clone in the command line. (Link to clone the project `https://github.com/flamxby/government.git`)
    ```
    cmd> git clone https://github.com/flamxby/government.git
    ```
## Instructions for setting up a virtual environment (virtualenv)
> **a virtual environment** is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them.
* Access to a command-line/terminal window.
    * Install a virtual environment.
        * Linux/MacOS:
            ```
            $ python3 -m pip install virtualenv
            ```
        * Windows:
            ```
            ...\> python -m pip install virtualenv
            ```    
    * Create new virtual environment.
        * Linux/MacOS:
            ```
            $ virtualenv venv
            ```
        * Windows:
            ```
            ...\> virtualenv env
            ``` 
    * Activate a virtual environment.
        * Linux/MacOS:
            ```
            $ source venv/bin/activate
            ```
        * Windows:
            ```
            ...\> env\Scripts\activate
            ``` 
* *See more details about [Running Python Apps in a Virtual Environment](https://cpske.github.io/ISP/django/virtualenv).*
## Steps needed to configure the application for running
* Access to a command-line/terminal window.
* Change directory to the directory that contain `government` folder.
    ```
    cmd> cd government
    ```
* Install the require packages for this project.
    ```
    cmd> pip install -r requirements.txt
    ``` 
    > Description of the require packages
    * **fastapi** is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
    * **uvicorn** is a lightning-fast ASGI server implementation, using uvloop and httptools.
    * **pytest** is a mature full-featured Python testing tool that helps you write better programs.
    * **requests** is a HTTP library for the Python programming language. The goal of the project is to make HTTP requests simpler and more human-friendly.
    * **gunicorn** is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model.
    * **coverage** is a tool for measuring code coverage of Python programs.
    * **sqlalchemy** is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
    * **passlib** is a password hashing library for Python 2 & 3, which provides cross-platform implementations of over 30 password hashing algorithms, as well as a framework for managing existing password hashes.
    * **bcrypt** is a key derivation function, which can be thought of as a special kind of hash function.
    * **python-jose** is collectively can be used to encrypt and/or sign content using a variety of algorithms. 
    * **python-multipart** is an Apache2 licensed streaming multipart parser for Python.
    * **python-dotenv** is a Python module that allows you to specify environment variables in traditional UNIX-like “.env” (dot-env) file within your Python project directory.
    * **gunicorn** is a Python Web Server Gateway Interface (WSGI) HTTP server.
    * **psycopg2** is a DB API 2.0 compliant PostgreSQL driver that is actively developed.

## How to start the application and verify it is working
1. **Clone** government project to your machine. [*See how to clone the project.*](https://github.com/flamxby/government/blob/master/INSTALL.md#how-to-clone-have-a-night-day-project)
2. Follows the [**setting up a virtual environment**](https://github.com/flamxby/government/blob/master/INSTALL.md#instructions-for-setting-up-a-virtual-environment-virtualenv).
3. Follows the [**steps needed to configure the application for running**](https://github.com/flamxby/government/blob/master/INSTALL.md#steps-needed-to-configure-the-application-for-running).
4. Access to a command-line/terminal window.
    * Change directory to the directory that contain `government` folder.
        ```
        cmd> cd government
        ```
    * ASGI server implementation
        * Linux/MacOS:
            ```
            $ uvicorn src.reservation.main:app --reload
            ```
        * Windows:
            ```
            ...\> uvicorn src.reservation.main:app --reload
            ``` 
            * Terminal window will show like this:
                ``` 
                INFO:     Will watch for changes in these directories: ['D:\\University\\3rd year\\Software Process & Project Management\\project\\code\\government']
                INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
                INFO:     Started reloader process [14616] using statreload
                INFO:     Started server process [7308]
                INFO:     Waiting for application startup.
                INFO:     Application startup complete.
                ``` 
    * Follows the link http://127.0.0.1:8000/docs

5. Quit the server
    * Exit the terminal window
        * Linux/MacOS: Press `CTRL + C` button
        * Windows: Press `CTRL + C` button
    
    * Deactivate virtualenv
        ```
        cmd> deactivate 
        ``` 
