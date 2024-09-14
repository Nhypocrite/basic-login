## Web Programming Assignment 02: Backend

---

#### Features 

- **User Registration**: Users can create accounts with a unique username and password.
- **User Login**: Users can log in with valid credentials, and sessions are managed using cookies.
- **"Remember Me" Option**: Sessions can be made persistent with a "Remember me" checkbox.
- **Session Management**: Sessions expire based on whether "Remember me" is selected.
- **Logout**: Users can log out, which clears their session.

This application provides a simple and secure user authentication flow with session management, ensuring users need to log in to access certain pages.

#### Behaviors

1. Homepage (`/`):
   - **Logged In**: Shows a personalized welcome message and a `Logout` button.
   - **Not Logged In**: Redirects to the login page.
2. Login Page (`/login`):
   - **Logged In**: Redirects to the homepage.
   - **Not Logged In**: Provides login form; allows "Remember me" option for extended session.
3. Registration Page (`/register`):
   - **Logged In**: Typically redirects to the homepage.
   - **Not Logged In**: Allows new users to register with a unique username.
4. Logout Action (`/logout`):
   - **Logged In**: Logs the user out, clears the session, and redirects to login.
   - **Not Logged In**: Redirects to the login page.



#### Prerequisites

##### 1. Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine

- MariaDB (or MySQL) installed and running
- Git installed

##### 2. Set up the virtual environment (**optional** but recommended)

You can create a virtual environment to manage dependencies:

```bash
python -m venv venv-ass2

# On Windows, run:
.\venv-ass2\Scripts\activate
# On Unix or MacOS, run:
source venv-ass/bin/activate

```

##### 3. Install dependencies

Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

##### 4. Set up the database

Login to MariaDB/MySQL:

```bash
mysql -u your_username -p

```

​	Create the database and tables:

```bash
MariaDB [(none)]>
MariaDB [(none)]> source ./users.sql;
MariaDB [(none)]>

```

Or, create table manually, see `users.sql`


##### 5. Configure the application

Open the app.py file and update the database connection configuration with your own credentials:

If you are using the default setting of MariaDB ( for example, using WinNMP), there's no need to change it. 

```python
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'web_programming'
}
```


##### 6. Run the application

You can now start the Flask application:

```bash
python app.py
```

Open your web browser and go to http://127.0.0.1:5000/ to view the website.





#### Assignment requirments:

##### Highlights:

"Remember me" (save session id in cookies, and restore the session on server side)

Both AJAX or "submit form and fresh page" are acceptable

Logout function is optional

##### original requirments:

implement a user system

Focus on backend functions, for frontend page only need two input form and buttons, for database please use officially MariaDB

Register a user with username and password, password must be stored as ciphertext

Login function should create a session on server side,

Logout function is optional

"Remember me" function is optional (save session id in cookies, and restore the session on server side)

Both AJAX or "submit form and fresh page" are acceptable

Please pack all your code into a ZIP file and upload to NTULearn.

Only light weight frameworks are acceptable(Flask, JQuery, Bootstrap)

Please also upload the SQL commands of table creation.

[Due: 23:59:00 16th Sep 2024 (Mon)]