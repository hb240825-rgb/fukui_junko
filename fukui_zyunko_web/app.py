from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# トップページ
@app.route("/")
def index():
    return render_template("index.html")

import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        opponent TEXT,
        score TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        opponent = request.form["opponent"]
        score = request.form["score"]
        date = request.form["date"]

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO results (opponent, score, date) VALUES (?, ?, ?)",
            (opponent, score, date)
        )

        conn.commit()
        conn.close()

        return "保存完了！ <a href='/results'>結果を見る</a>"

    return render_template("result_form.html")

@app.route("/results")
def results():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM results")
    data = cur.fetchall()

    conn.close()

    return render_template("results.html", data=data)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    import sqlite3
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    if request.method == "POST":
        opponent = request.form["opponent"]
        score = request.form["score"]
        date = request.form["date"]

        cur.execute(
            "UPDATE results SET opponent=?, score=?, date=? WHERE id=?",
            (opponent, score, date, id)
        )
        conn.commit()
        conn.close()

        return redirect("/results")

    cur.execute("SELECT * FROM results WHERE id=?", (id,))
    data = cur.fetchone()
    conn.close()

    return render_template("edit.html", data=data)

@app.route("/delete/<int:id>")
def delete(id):
    import sqlite3
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM results WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/results")

if __name__ == "__main__":
    app.run(debug=True)