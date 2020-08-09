# MESSAGE BOARD
"Message board" is a web application that allows registered users to have conversations about different topics.

"Message board" is also a practical work for the University of Helsinki's Department of Computer Science: Database application course ([TKT20011](https://hy-tsoha.github.io/materiaali/index)).

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
* Create, remove and hide different categories
* Remove threads

#### User can:
* Register a new user
    * Required information:
        * username
        * email
        * password
* Edit users own registration details
* Remove users own data
* Create new threads to different categories
* Send new messages to threads
* Edit users own messages
* Remove users own messages

#### Common features (without registering):
* Browse and read non hidden threads and messages
* Search threads and messages

## PREREQUISITES
* Python 3.x
    * Dependencies listed in the projects requirements.txt (for auto install)
        * flask
        * flask_sqlalchemy
        * flask_wtf
        * flask-Sessions
        * flask-Login
        * psycopg2
        * python-dotenv
* PostgreSQL

## AUTHOR
Teemu Bergman

## LICENSE
Distributed under the MIT License. See `LICENSE` for more information.
