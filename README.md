Bingeable
#### Video Demo:  https://www.youtube.com/watch?v=n25xmH8tAVY
#### Description: A flask webapp for creating comic book "reading lists"
Bingeable is a relatively simple flask webapp for creating comic book reading lists.

The Problem:
Inspired by "The Comic Book Herald" i am currently reading the "top" or "most important" 10 storylines from each year of marvel's history starting in 1961 with the release of Fantastic Four #1 going year by year upto the present.
To track the issues i've read i created a excell sheet, and once i did that i added fields to track who was the writer and artist on each issue.

Solution:
Take that simple excell sheet and turn it into a more robust webapp utilizing dynamic code and SQL to create a framework to organize the data in an improved way and the flexibility to improve upon in the future.


How:

Database
As tought by CS50 i used Sqlite3. This might not be the most robust version of SQL but it suits this limited project just fine, if i end up growing it i might consider porting it to MySQL but that is not needed for this project.
I made a single database file "comics.db" that contains all the backend data needed for this project, when designing the database i used the drawsql.app webapp to get a graphical representation of the database, this made implementing it much easier.

    Tables:
        in most of these tables i store more information than is used in this project, i decided to to that so that if i ever wanted to expand on the project the data would already be available.
        comic_series
            This table holds the information on each series or "run" of comic books. I.E; Fantastic Four, Spider-Man, Avengers etc etc.
            In addition to the name which is the only thing actually used in the project currently i also store the year of first publication this is used to seperate volumes of series of the same name I.e (Fantastic Four (1961) vs Fantastic Four (2018))
            I also store a description with the intent of possibly adding a detail page about the series where things like that are displayed, this was not needed for this project but will be needed immediately if the project expands.
            I store a image (by storing the path to the image saved on the server) for the same reason, lastly i store the relative id of the publisher from the publisher table to assosiate a publisher for the series (Ie. Fantastic Four published by Marvel)

        binges
            "Binges" are what i call my reading lists. And it is up to the user how to use these, you could have one big binge with hundreds of comics or several smaller ones. That is entirely up to how the user wants to organize their reading lists, and this table store the information assosiated with that.
            In this fairly small table i store a "Title" for a binge the id of the user that created the binge and the id of every comic in that binge.

        publishers
            This table is super simple, mostly because there arent that many publishers to re-implementing this table for any expanded scope would be super simple. and this table is techinically not used in the project except for some relational assosiation.
            So in this table i only store the name of the publisher and an image.

        writers
            In this table i store the name of each writer, a description and an image. This is most of the information i needed for this project. If i were to expand it i would have stored date of birth/death and nationality as well.
        artists
            This is exactly the same as for writers, in hindsight i might have made a "people" table instead and somehow stored wether they were writers or artists instead of doing everything twice, but this was simple enough.
        users
            This is the table used for registered users, as such the only things i store here (other than the id ofcourse) is a hashed password and an image, i don't use profile pictures in this project so that is just for future possibilities.
        readinglist
            This is the meat and potatoes of the whole app. The whole page is built around this table so everything else feeds into this or presents the data from this.
            This table could probably better be called "issue" to better represent what it actially does, but the name is an artifact of less than perfectly planned development.
            in this table i store the issue number of the issue (Fantastic Four #1, Fantastic Four #2 etc.) the id of the user that created this issue in one of their binges.
            the id of the comic_series that this is a issue of. the id of the writer and the artist that worked on this issue. a bool value (in this case just integer 1 or 0) of weither the user has read the issue or not.
            a description, and a image.
            and lastly the id of the bindge that this comic is sorted under.


helpers.py
    This started out as a larger file where i brought over most of the code from the helpers.py but the only thing i kept was the login_required. Everything else i ended up re-implementing in a different way.
    So this just has the code that redirects to login if the user tries to access any page other than login or register while not being logged in.

index.html
    this is the main site. (obviously).
    When you first register this will be mostly empty. but as soon as you add a binge and start adding issues to it this is where all the "action" is at. with this file i dynamically create a list of binges each containing a list of issues all retrieved from the database using the logged in users id.

addissue.html
    you get to this page from the "add issue" button assosiated with each binge. Doing it this way i can easily get the id of the binge the issues need to be assosiated with. When you fill in all the information asked on this page you will be redirected to the home page and the new issue will be added to the list.

layout.html
    This page is mostly the navigation menu, the options on the menu changes depending on if you are logged in or not.

profile.html
    this page is accessed by clicking on the name of a writer or artist on the main page. that brings you to a profile page for that person, showing a picture if added, their name and any comic books in your binges assosiated with them.

register.html
    a simple registration form, this was mostly copied from the solution for the finance problem set.

login.html
    Similar with the register.html this was mostly just a copy pase from the fintance problem set solution.
binge.html

publishers.html
    this page lets you enter the information about a publisher into the database.

writers.html
    this page lets you enter the information about a writer into the database.
artists.html
    this page lets you enter the information about an artist into the database.
series.html
    just like the previous ones, this page lets you enter the information about a particular series into the database.

app.py
    This file handles all the routing for the page. there arent any super complex logic or code in there since most of the pages are either entering data into a database or retreiving data from a database.

styles.css
    I did use boostrap for this project to handle most of my frontend stuff, which i made more of a hazzle than it probably needed to be but i'm not a frontend guy. What little custom css i did do was mostly to do with link colors (and hover), the profile images and the read/not read display is entirely css.


Conclusion
    I wanted to do a webapp simply because it's the subject from CS50x i'm the least familiar with, i could have just made a game but i've made so many of them already it would have been less of a challenge.
    So when i decided i wanted to make a webapp i needed to figure out what problem i wanted to solve, and i am curently in the middle of a massive marvel comics project, of reading 10 stories from each year of marvels history. and then listening to a great podcast by The Comic Book Herald called "My Marvelous Year" where the hosts do the same.
    Is this solution better than a simple excell sheet? I don't know. but it was a challenging project that i learned a lot from. And i think if i gave this project a couple of months instead of weeks. And built it out a lost more it could have a lot of potential. But as it stands its a niche solution to a niche problem.
    I will attemt to host this project in aws (and in the process learn how that is done) and use it for continuing my reading project and we'll see if i found it usefull or not.