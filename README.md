# Kanban Tasker using Flask

Kanban Tasker is a web application designed to help you manage your tasks. It has 4 sections - To Do, In Progress, In Review and Done. This has been designed using HTML, CSS, Bootstrap and powered by the Flask micro-framework and Firebase.  
This is one of my personal projects developed over a weekend.  
To check out more of my projects, visit my [Github profile](https://github.com/romeo611199/) or my [Portfolio website](https://romaxrajeev.in).

## How to use this Kanban Tasker App

Check out the [application](https://kanban-tasker-flask.herokuapp.com/) deployed on Heroku.  

If you want to explore how this application is designed and structured, please follow the steps below:

1. Clone or download this repository.  
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries, in a virtual environment.

```bash
pip install -r requirements.txt
```
3. Set up a project in [Firebase](https://firebase.google.com/) and get the credentials. Keep all of those in a separate file and import into app.py file.
4. Set up Authentication with Email and Password, so that Firebase can authenticate the users.
5. Run app.py in the console to start up the server.

```bash
python app.py
```


## Contributing
Pull requests are welcome. Open an issue first, and then after verification, it would be added to the final repository.

## License
This project is licensed under [MIT](https://github.com/romeo611199/kanban-tasker-flask/blob/main/LICENSE) license.
