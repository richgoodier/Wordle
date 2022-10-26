import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, perc

import random

db = SQL("sqlite:///wordledb.db")

#db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, one_guess INTEGER DEFAULT 0, two_guess INTEGER DEFAULT 0, three_guess INTEGER DEFAULT 0, four_guess INTEGER DEFAULT 0, five_guess INTEGER DEFAULT 0, six_guess INTEGER DEFAULT 0, seven_guess INTEGER DEFAULT 0, wins INTEGER DEFAULT 0, games INTEGER DEFAULT 0)")

'''
outputString = [["", "", "", "", ""]] * 6

allword = ["crane", "tough", "blips", "fourt", "fifth", "final"]
guess_word = "crane"
temp = []
print(f"temp: {temp}")
outputString = [["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""]]
guess = 0

for guess in range(6):
    guess_word = allword[guess]
    for i in range(5):
        outputString[guess][i] = guess_word[i].upper()

print(f"outputString: {outputString}")


old_wins = db.execute("SELECT wins FROM users WHERE id = ?", 1)
print(old_wins)
print(old_wins[0]["wins"])

stats = db.execute("SELECT * FROM users WHERE id = ?", 1)
print(stats[0]["one_guess"])

'''
stats = db.execute("SELECT * FROM users WHERE id = 1")[0]
print(stats)

username = stats["username"]
print(username)

print((stats["games"]))


losses = ((stats["games"]) - (stats["wins"]))
total_guesses = (stats["one_guess"]) + (2 * stats["two_guess"]) + (3 * stats["three_guess"]) + (4 * stats["four_guess"]) + (5 * stats["five_guess"]) + (6 * stats["six_guess"]) + (7 * losses)
if stats["games"] == 0:
    stats["average_guesses"] = 0
    stats["win_percentage"] = 0.00
else:
    stats["average_guesses"] = 1.00 * (total_guesses) / (stats["games"])
    stats["win_percentage"] = 100.00 * ((stats["wins"]) / (stats["games"]))
print(losses)

