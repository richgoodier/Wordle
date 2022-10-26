import random
from operator import itemgetter

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, perc

# For the Wordle Game
import random
random.seed()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["perc"] = perc

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///wordledb.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show rankings"""
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = name[0]["username"]
    # Update price of all stocks with lookup function

    # Load user_stats table in stock_stats
    user_list = db.execute("SELECT * FROM users")

    # Create and populate dictionary with Name, Average Guesses, Games Played, Win Percentage
    final_user_stats = []
    for row in user_list:
        current_user = {}
        current_user["name"] = (row["username"])
        current_user["games"] = (row["games"])

        losses = ((row["games"]) - (row["wins"]))
        total_guesses = (row["one_guess"]) + (2 * row["two_guess"]) + (3 * row["three_guess"]) + (4 * row["four_guess"]) + (5 * row["five_guess"]) + (6 * row["six_guess"]) + (7 * losses)
        if row["games"] == 0:
            current_user["average_guesses"] = 0
            current_user["win_percentage"] = 0.00
        else:
            current_user["average_guesses"] = 1.00 * (total_guesses) / (row["games"])
            current_user["win_percentage"] = 100.00 * ((row["wins"]) / (row["games"]))

        final_user_stats.append(current_user)

        sortedUserStats = sorted(final_user_stats, key=itemgetter("win_percentage"), reverse=True)

    return render_template("index.html", username=username, sortedUserStats=sortedUserStats)


@app.route("/stats")
@login_required
def stats():
    """Show rankings"""
    stats = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    username = stats["username"]

    losses = stats["games"] - stats["wins"]
    stats["losses"] = losses

    total_guesses = (stats["one_guess"]) + (2 * stats["two_guess"]) + (3 * stats["three_guess"]) + (4 * stats["four_guess"]) + (5 * stats["five_guess"]) + (6 * stats["six_guess"]) + (7 * losses)
    if stats["games"] == 0:
        stats["average_guesses"] = 0
        stats["win_percentage"] = 0.00
    else:
        stats["average_guesses"] = 1.00 * (total_guesses) / (stats["games"])
        stats["win_percentage"] = 100.00 * ((stats["wins"]) / (stats["games"]))

    return render_template("stats.html", username=username, stats=stats)



@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    """Play Wordle!"""
    global correct_word
    global guesses
    global outputString
    global all_outputs
    global guessed_words
    global legalWords
    global youWin

    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = name[0]["username"]

    if request.method == "POST":

        guess_word = request.form.get("guess_word").lower()

        # Checks if guess_word is a legal word
        if (guess_word not in legalWords):
            errorMessage = "Not a legal word"
            return render_template("play.html", errorMessage=errorMessage, outputString=outputString, all_outputs=all_outputs, guesses=guesses, correct_word_cap=correct_word.upper(), username=username, youWin=youWin)

        # Check if guess_word was already used
        if (guess_word in guessed_words):
            errorMessage = "Word already tried"
            return render_template("play.html", errorMessage=errorMessage, outputString=outputString, all_outputs=all_outputs, guesses=guesses, correct_word_cap=correct_word.upper(), username=username, youWin=youWin)

        guessed_words.append(guess_word)

        # Check guess_word is the correct_word
        if guess_word in correct_word:
            youWin = 1

            # Update Wins
            old_wins = db.execute("SELECT wins FROM users WHERE id = ?", session["user_id"])
            new_wins = old_wins[0]["wins"] + 1
            db.execute("UPDATE users SET wins = ? WHERE id = ?", new_wins, session["user_id"])

            # Update Games Played
            old_games = db.execute("SELECT games FROM users WHERE id = ?", session["user_id"])
            new_games = old_games[0]["games"] + 1
            db.execute("UPDATE users SET games = ? WHERE id = ?", new_games, session["user_id"])

            # Update guesses
            stats = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
            if guesses == 0:
                new_guess = stats[0]["one_guess"] + 1
                db.execute("UPDATE users SET one_guess = ? WHERE id = ?", new_guess, session["user_id"])
            elif guesses == 1:
                new_guess = stats[0]["two_guess"] + 1
                db.execute("UPDATE users SET two_guess = ? WHERE id = ?", new_guess, session["user_id"])
            elif guesses == 2:
                new_guess = stats[0]["three_guess"] + 1
                db.execute("UPDATE users SET three_guess = ? WHERE id = ?", new_guess, session["user_id"])
            elif guesses == 3:
                new_guess = stats[0]["four_guess"] + 1
                db.execute("UPDATE users SET four_guess = ? WHERE id = ?", new_guess, session["user_id"])
            elif guesses == 4:
                new_guess = stats[0]["five_guess"] + 1
                db.execute("UPDATE users SET five_guess = ? WHERE id = ?", new_guess, session["user_id"])
            elif guesses == 5:
                new_guess = stats[0]["six_guess"] + 1
                db.execute("UPDATE users SET six_guess = ? WHERE id = ?", new_guess, session["user_id"])

        # Add guess_word to outputString
        for i in range(5):
            outputString[guesses][i] = guess_word[i].upper()

        # Create Lists to track which letters are a match
        c_word_clone = ["-"] * 5
        for i in range(5):
            c_word_clone[i] = correct_word[i]

        guess_clone = ["-"] * 5
        for i in range(5):
            guess_clone[i] = guess_word[i]

        # Set output
        output = ["grey"] * 5

        # Check if letters match (GREEN).
        for i in range(5):
            if guess_clone[i] == c_word_clone[i]:
                output[i] = "green"
                guess_clone[i] = "+"
                c_word_clone[i] = "-"

        # Check if letters match (YELLOW).
        for j in range(5):
            for i in range(5):
                if guess_clone[i] == c_word_clone[j]:
                    output[i] = "yellow"
                    guess_clone[i] = "+"
                    c_word_clone[j] = "-"

        # Add output to all_outputs
        for i in range(5):
            all_outputs[guesses][i] = output[i]

        guesses += 1

        # If you run out of guesses
        if guesses == 6 and youWin != 1:
            stats = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

            # Update guesses
            new_guess = stats[0]["seven_guess"] + 1
            db.execute("UPDATE users SET seven_guess = ? WHERE id = ?", new_guess, session["user_id"])

            # Update games played
            new_games = stats[0]["games"] + 1
            db.execute("UPDATE users SET games = ? WHERE id = ?", new_games, session["user_id"])

        return render_template("play.html", outputString=outputString, all_outputs=all_outputs, guesses=guesses, correct_word_cap=correct_word.upper(), username=username, youWin=youWin)

    else:
        outputString = [["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""]]
        all_outputs = [["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""]]
        guesses = 0
        guessed_words = []
        youWin = 0

        with open("wordle-answers-alphabetical.txt", "r") as file:
            allText = file.read()
            words = list(map(str, allText.split()))
            correct_word = random.choice(words)

        with open("wordle_list.txt", "r") as file:
            allText = file.read()
            legalWords = list(map(str, allText.split()))

        name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = name[0]["username"]
        return render_template("play.html", guesses=guesses, correct_word=correct_word, outputString=outputString, all_outputs=all_outputs, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        username = request.form.get("username")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Validate submission
    if request.method == "POST":

        # Ensure username is submitted
        if not request.form.get("username"):
            return apology("username needed")

        # Ensure username is not used
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("username taken")

        # Ensure password and password_clone are submitted
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("password needed")

        # Ensure password and password_clone identical
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password mismatch")

        # SUCCESS!!!

        # Create personal stock porfolio db for user
        username = request.form.get("username")

        # Register New User
        hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

