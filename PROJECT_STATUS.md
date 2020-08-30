## PROJECT STATUS

#### 30.08.2020
* Added alert messages
* Clear your old browser cookie from this site, otherwise there might be problems.
* Application maximum width is now 840px
* Cleaned up SQL query syntax.
* Role based authorization implemented. Roles: **USER**, **SECRET**, **BANNED**, **DELETED** and **ADMIN**.
    * This also means that users cannot see what they aren't supposed to see.
* When text is send to the back end it is cleaned up from unnecessary whitespace.
* Admin panel revamp.
* User profile page revamp.
* Added CSRF tokens everywhere.

Test with demo users:
* admin@messageboard.com / admin
* john.doe@messageboard.com / johndoe
* jane.doe@messageboard.com /janedoe


#### 23.08.2020
**Use demo user credentials (above) to view three different user scenarios.**

User functionality:
* Profile
    * Register a new user.
    * Edit users own registration details.
    * Remove users own profile.
* Message board
    * Create new threads to different categories.
    * Send new messages to threads.
    * Edit users own messages.
    * Remove users own messages (if last message also thread is deleted).
    * View hidden categories (if user has the rights).
    * Search keywords from messages (not on secret categories at the moment).
    
Admin functionality:
* Admin panel
    * View all users and their account data (except passwords).
    * Add or remove rights for secret categories.
    * Add or remove admin rights.
    * Ban or remove ban an account.
    * Delete on revive an account.

ToDo:
- Finish admin control panel (It's a bit of a mess now).
- Implement role base authorization (Now admin side is a hack).
- Clean up HTML and CSS to make the app nicer looking.


#### 09.08.2020
At the moment the Message Board -application can be tested at: [messageboard-tb.herokuapp.com](http://messageboard-tb.herokuapp.com) and its current features are:
- User can register, login and logout.
- User can create new threads.
- User can post/reply to threads.
- User can view its personal date.