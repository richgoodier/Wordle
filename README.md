# COMPETITIVE WORDLE WEBSITE
#### Video Demo: <https://youtu.be/MBog-2T3CHs>
### Description:
Welcome to my Competitive Wordle Website!

Wordle is a simple word game that can be played on the [NYTimes website] (https://www.nytimes.com/games/wordle/index.html).  Unfortunately, you are unable to see how friends compare to you.

My Competitive Wordle Website allows you to play the original game while also seeing how you rank relative to your friends.

#### register.html
First, you must register with a username and password.  The information is saved in wordledb.db in a table called “users” for future use and to track stats.

#### login.html
While the website does save your session, you can login anytime.

#### index.html
The main page shows the rankings of all players, including average number of guesses per game, total games played, and current win percentage.  The rankings are ordered by win percentage.

#### stats.html
If you are interested in more personal stats, this page offers a more granular breakdown.

#### apology.html
This site communicates to the user any errors

#### helpers.py
This file contains a few functions, one for apology, one to decorate routes to require login, and a simple one to render a float into a percentage with two significant digits (for stats and rankings).

#### wordle_list.txt
In order to create a Wordle game, I needed a list of 5-letter English words.  I took the large.txt from pset5: speller and filtered out all the 5-letter words that contained only alphabetical characters.  This list would serve as my list of legal words that a player could submit.

#### wordle-answers-alphabetical.txt
Next, I found online a txt file that purportedly is the list of words that Wordle uses to pull from for the daily correct word.  It is a hand-curated list and is a subset of my legal words.

#### appy.py
This file manages the registration, login, and organizing the stats onto the webpages, but more importantly this is where the logic of the game can be found, in the play() function.

##### play()
Wordle is a simple game to play, but a little more complicated to code.  When you guess a word, play() needs to do a number of things:
1. Determine if a letter is in the correct position (Green)
2. Determine if a letter is in the correct word but in the incorrect position (Yellow)
3. Determine in a letter is not in the correct word
4. Manage duplicate letters in the guessed word and correct word

play() then saves all the guessed words so far in a list called outputString as well as the results of determining whether letters should be designated green, yellow, or grey in a list called all_outputs.  Both are passed variables are passed to play.html where the board is updated.

If the player succeeds/fails in guessing the correct word within six guesses, their stats are updated in the “users” table, and play.html will render with a success or failure message, offering the user to play again.

#### play.html
This page creates a table with a row for each guess and a cell in each row for each letter, just like the original game.  There is a text box to type in the guess.  When play() returns the proper variables, play.html uses jinja to fill in the letters and colors in their proper place.

#### Conclusion
And that’s it!  You can now play Wordle and see how your friends compare, pushing one another to play the game even better than before!

#### Future Work
- I would like to make this website live on the www so that it can actually be used!
- I would like to make the game a bit more user-friendly by including a keyboard that color-code the letters along the way.
- I am in the process of creating a number of WordleBots that use various algorithms.  I plan to place them among the rankings so human players can see how they compare to these bots.