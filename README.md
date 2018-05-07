# peewee-notes
Note taking apps with authorize acoording to this tutorial http://charlesleifer.com/blog/saturday-morning-hack-a-little-note-taking-app-with-flask/

Based on the Flask framework with postgresql database on peewee orm. App requires authentication for every request. Design of notes are made according to the 	
forementioned tutorial, GUI of note page allows to add some styles to the text like bold, italic, indention, and notes are placed via Masonry grid. Used Micawber to display an extended content of urls.  
Forms are implemented via Flask-WTF extension and all data is transmitted through the Jinja placeholders. Also there are user page with where it possible to change some user data and profile photo. Photos are uploaded from the disk and are saved into the project repo with name that was created by hashing user email and saved to the database. 
