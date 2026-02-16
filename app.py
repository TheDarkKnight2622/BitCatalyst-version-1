
# Structure inspired by the finance problem set

import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import sqlite3
from helpers import error, login_required, usd, live


app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///bit.db")

# To configure the tables in the database


def db_init():
    conn = sqlite3.connect('bit.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS
                 recovery (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 name TEXT NOT NULL,
                 seed_phrase TEXT NOT NULL
                 ) ''')

    c.execute('''CREATE TABLE IF NOT EXISTS
                 transactions (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 symbol TEXT,
                 size INTEGER,
                 opening_price NUMERIC,
                 direction TEXT,
                 closing_price NUMERIC,
                 pnl NUMERIC,
                 timestamp DATETIME,
                 FOREIGN KEY(user_id) REFERENCES users(id)
                 ) ''')
    c.execute('''CREATE TABLE IF NOT EXISTS
                 holdings (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 price NUMERIC,
                 symbol TEXT,
                 direction TEXT,
                 size INTEGER,
                 FOREIGN KEY(user_id) REFERENCES users(id)
                 ) ''')

    c.execute(''' CREATE TABLE IF NOT EXISTS
              users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                hash TEXT NOT NULL,
                cash NUMERIC NOT NULL DEFAULT 5000
                 ) ''')

    c.execute(''' CREATE TABLE IF NOT EXISTS
                  journal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    page TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                    ) ''')

    conn.commit()
    conn.close()


db_init()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# index route. The deafult option being the landing page, pre-login. The index page also displays a table of open transactions that the users can close.
# inside the table is a form that submitted anytime the 'close' button is clicked in any row of the table. The user's balance is then updated, along with the trade being filed into the transactions table and being deleted from holdings.


@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user_id"):
        if request.method == "POST":
            close1 = request.form.get("ident1")
            close2 = request.form.get("ident2")
            close3 = request.form.get("ident3")
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
            if close2 == 'short':
                og = db.execute("SELECT price FROM holdings WHERE symbol= ? AND user_id=? AND direction = ?",
                                close1, session['user_id'], close2)[0]["price"]
                delta = og - live(close1)
                close3 = float(close3)
                pnl1 = delta * close3
                db.execute("UPDATE users SET cash= ?", cash + ((delta * close3)) + (og * close3))
                time = datetime.datetime.now()
                db.execute("INSERT INTO transactions (symbol, direction, size, opening_price, closing_price, timestamp, pnl, user_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                           close1, close2, close3, og, live(close1), time, pnl1, session['user_id'])
                db.execute("DELETE FROM holdings WHERE user_id= ? AND symbol= ? AND direction = ?",
                           session["user_id"], close1, close2)
                flash("Done!")
                return redirect('/')
            else:
                og = db.execute("SELECT price FROM holdings WHERE symbol= ? AND user_id=? AND direction = ?",
                                close1, session['user_id'], close2)[0]['price']
                delta = live(close1) - og
                close3 = float(close3)
                pnl2 = delta * close3
                db.execute("UPDATE users SET cash= ?", cash + (live(close1) * close3))
                time = datetime.datetime.now()
                db.execute("INSERT INTO transactions (symbol, direction, size, opening_price, closing_price, timestamp, pnl, user_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                           close1, close2, close3, og, live(close1), time, pnl2, session['user_id'])
                db.execute("DELETE FROM holdings WHERE user_id= ? AND symbol= ? AND direction = ?",
                           session["user_id"], close1, close2)
                flash("Done!")
                return redirect('/')
        else:
            holdings = db.execute("SELECT * FROM holdings WHERE user_id= ?", session["user_id"])
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            starting_cash = cash[0]["cash"]
            return render_template("index.html", holdings=holdings, cash=starting_cash)
    else:
        return render_template("landing.html")

# Standard registeration page route, with failsafes in case of empty fields.


@app.route("/register", methods=["GET", "POST"])
def register():
    if request. method == 'POST':
        if request.form.get('confirmation') != request.form.get('password'):
            return error("Password and confirmation do not match", 400)

        elif not request.form.get('username'):
            return error("Please fill in a username", 400)

        elif not request.form.get('password'):
            return error("Please fill in a password", 400)

        elif db.execute('SELECT username FROM users WHERE username = ?', request.form.get('username')):
            return error('Username taken', 400)

        else:
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            seed = request.form.get('seed')
            db.execute('INSERT INTO users (username, hash) VALUES (?, ?)',
                       username, generate_password_hash(password))
            db.execute('INSERT INTO recovery (seed_phrase, username, name) VALUES (?, ?, ?)',
                       seed, username, name)

            return redirect('/')
    else:
        return render_template("register.html")


# Standard login procedure.
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return error("must provide username", 403)

        elif not request.form.get("password"):
            return error("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return error("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

# For the user to perform a manual sign-out through the navbar catalogue


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# A reset route in case a user forgets their password, where this page serves as verification. They will user their unique seed to perform the reset.


@app.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == 'POST':
        username = request.form.get('username')
        seed = request.form.get('seed')
        rows = db.execute("SELECT username, seed_phrase FROM recovery WHERE username = ?", username)
        if not seed or not username:
            return error("You have have not completed the form", 400)
        else:
            if len(rows) != 1 or rows[0]["seed_phrase"] != seed:
                return error("You have have keyed in the wrong credentials", 400)
            else:
                return render_template('postreset.html')
    else:
        return render_template('reset.html')

# A follow-up page for users upon confirmation of their identity to set a new password.


@app.route("/postreset", methods=["GET", "POST"])
def postreset():
    if request.method == 'POST':
        passwrd = request.form.get('passwrd')
        conf = request.form.get('confirmation')
        username = request.form.get('username')
        if not passwrd or not conf:
            return error("You have not completed the form", 400)
        elif passwrd != conf:
            return error("Your new password and repeat do not match", 400)
        else:
            db.execute('UPDATE users SET hash = ? WHERE username = ?',
                       generate_password_hash(passwrd), username)
            flash('Reset successful!')
            return redirect('/')

# A custom profile page where users can withdraw/deposit in-platform currency. Upon reception of their desired amount,the appropriate transactions are performed.


@app.route("/profile", methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'POST':
        dep = request.form.get("amount1")
        wit = request.form.get("amount2")
        if dep:
            db.execute('UPDATE users SET cash = cash + ? WHERE id = ?', dep, session["user_id"])
            flash("Deposit Successful!")
            return redirect('/')
        elif wit:
            balance = db.execute('SELECT cash FROM users WHERE user_id = ?',
                                 session["user_id"])[0]['cash']
            if wit < balance:
                db.execute('UPDATE users SET cash = cash - ? WHERE user_id = ?',
                           dep, session["user_id"])
                flash("Withdrawal Successful!")
                return redirect('/')
            else:
                return error("You do not have sufficient funds to perform this transaction", 400)
        else:
            return error("Your submission was unsuccessful", 400)
    else:
        name = db.execute('SELECT username FROM users WHERE id=?',
                          session['user_id'])[0]['username']
        return render_template('profile.html', name=name)

# A page where users can evaluate their trades, Done by calculating a few metrics from the transactions table and displaying them entriely.


@app.route("/analyse")
@login_required
def analyse():
    ptns = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        session["user_id"]
    )

    avg = db.execute(
        "SELECT AVG(pnl) AS avg_pnl FROM transactions WHERE user_id = ?",
        session["user_id"]
    )[0]["avg_pnl"]

    win = db.execute(
        "SELECT COUNT(*) AS c FROM transactions WHERE pnl > 0 AND user_id = ?",
        session["user_id"]
    )[0]["c"]

    lose = db.execute(
        "SELECT COUNT(*) AS c FROM transactions WHERE pnl <= 0 AND user_id = ?",
        session["user_id"]
    )[0]["c"]

    rate = (win / (win + lose) * 100) if (win + lose) else 0

    daily = db.execute("""
        SELECT
          DATE(timestamp) AS day,
          SUM(pnl) AS total_pnl
        FROM transactions
        WHERE user_id = ?
        GROUP BY DATE(timestamp)
        ORDER BY day ASC
    """, session["user_id"])

    top_coins = db.execute("""
    SELECT
        symbol,
        COUNT(*) AS trades,
        SUM(pnl) AS total_pnl
    FROM transactions
    WHERE user_id = ?
    GROUP BY symbol
    ORDER BY total_pnl DESC
    LIMIT 5
    """, session["user_id"])


    labels = [row["day"] for row in daily]
    values = [float(row["total_pnl"] or 0) for row in daily]

    return render_template(
        "analyse.html",
        ptns=ptns,
        avg=avg or 0,
        rate=rate,
        labels=labels,
        values=values,
        top_coins=top_coins
    )

# Page to perform trades. Symbol, price and direction are pulled and saved into the holdings table, while relevant deductions are made to the user's balance.


@app.route("/trade", methods=['POST', 'GET'])
def trade():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        direction = request.form.get("direction")
        position_str = request.form.get("position")

        if not symbol or not direction or not position_str:
            return error("Oops! Ensure that you filled in every field", 400)

        try:
            position = float(position_str)
        except ValueError:
            return error("Position must be a number", 400)

        rows = db.execute(
            "SELECT symbol, price, direction, size FROM holdings WHERE user_id = ?",
            session["user_id"]
        )
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            session["user_id"]
        )[0]["cash"]

        live_price = live(symbol)

        found = False
        for row in rows:
            if row["symbol"] == symbol and row["direction"] == direction:
                old_price = row["price"]
                old_size = row["size"]
                new_size = old_size + position
                new_price = ((old_price * old_size) + (live_price * position)) / new_size

                db.execute(
                    "UPDATE holdings SET price = ?, size = ? WHERE user_id = ? AND symbol = ? AND direction = ?",
                    new_price,
                    new_size,
                    session["user_id"],
                    symbol,
                    direction
                )
                db.execute(
                    "UPDATE users SET cash = ? WHERE id = ?",
                    cash - live_price * position,
                    session["user_id"]
                )
                found = True
                break

        if not found:
            # no existing row with same symbol+direction → create new
            db.execute(
                "INSERT INTO holdings (user_id, price, symbol, direction, size) VALUES (?, ?, ?, ?, ?)",
                session["user_id"],
                live_price,
                symbol,
                direction,
                position
            )
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                cash - live_price * position,
                session["user_id"]
            )

        return redirect("/")


    return render_template("trade.html")


# User logs entries daily through this page. Entries are then displayed by accessing the journal table,
@app.route("/journal", methods=["GET", "POST"])
@login_required
def journal():
    if request.method == "POST":
        entry = request.form.get("j-sub")

        if not entry or not entry.strip():
            return error("Please write something in your journal.", 400)

        db.execute(
            "INSERT INTO journal (user_id, page) VALUES (?, ?)",
            session["user_id"],
            entry.strip()
        )

        return redirect("/journal")

    entries = db.execute(
        """
        SELECT
            page,
            strftime('%Y-%m-%d', created_at) AS created_date
        FROM journal
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        session["user_id"]
    )

    return render_template("journal.html", entries=entries)
