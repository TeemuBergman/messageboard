# MESSAGE BOARD
"Message board" is a web application that allows registered users to have conversations about different topics.

"Message board" is also a practical work for the University of Helsinki's Department of Computer Science: Database application course ([TKT20011](https://hy-tsoha.github.io/materiaali/index)).

Demo: [messageboard-tb.herokuapp.com](messageboard-tb.herokuapp.com)

## STATUS

#### 23.08.2020
User functionality:
* Profile
    * Register a new user
    * Edit users own registration details
    * Remove users own profile
* Message board
    * Create new threads to different categories
    * Send new messages to threads
    * Edit users own messages
    * Remove users own messages (if last message also thread is deleted)
    * View hidden categories (if user has the rights)

ToDo:
- Create admin control panel (functionality is there, but HTML is undone at the moment)
- Clean up HTML and CSS to make the app nicer looking


#### 09.08.2020
At the moment the Message Board -application can be tested at: [messageboard-tb.herokuapp.com](messageboard-tb.herokuapp.com) and its current features are:
- User can register, login and logout
- User can create new threads
- User can post/reply to threads
- User can view its personal date

## FEATURES

#### Application enables:
* Users to:
    * Control their personal data
    * Add threads and post messages to them
* Admins to:
    * Control registered user data and their permissions
    * Control message boards categories

#### Administrator can:
* Remove users
* Change user rights to admin or user
* Remove user rights (ban) temporarily or permanently
* Add a special right for specific user to view a hidden categories
* Create, remove and hide (secret) different categories
* Remove threads

#### User can:
* Register a new user
    * Required information:
        * username
        * email
        * password
* Edit users own registration details
    * Email
    * Password
* Remove users own profile
* Create new threads to different categories
* Send new messages to threads
* Edit users own messages
* Remove users own messages
* View hidden categories (if user has the rights)

#### Common features (without registering):
* Browse and read non hidden threads and messages
* Search threads and messages

## PREREQUISITES
* Python 3.x
    * Dependencies listed in the projects requirements.txt (for auto install)
        * gunicorn
        * flask
        * flask-login
        * flask-admin
        * flask_sqlalchemy
        * SQLAlchemy
        * psycopg2
        * python-dotenv
        * Werkzeug
        * PostgreSQL

## AUTHOR
Teemu Bergman

## LICENSE
Distributed under the MIT License. See `LICENSE` for more information.
