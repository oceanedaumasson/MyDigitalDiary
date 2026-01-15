from flask import Flask, render_template, request, session, redirect, url_for
from openai import OpenAI
import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Make true to test with entry limit
editMode = False

@app.route("/write", methods=["GET", "POST"])
def write():
    date = datetime.datetime.now().strftime("%b %d, %Y")
    response = None

    if "conversation" not in session:
        session["conversation"] = []
        session["entryCount"] = 0

    if not editMode and session["entryCount"] >= 45:
        response = "Sorry! You've reached the maximum of 45 entries."
        session["conversation"].append(
            {"role": "assistant", "content": response}
        )

    elif request.method == "POST":
        entry = request.form.get("entry")

        if entry:
            session["conversation"].append(
                {"role": "user", "content": entry}
            )
            session["entryCount"] += 1

            try:
                 
             system_prompt = {
                    "role": "system",
                    "content": (
                        "Imagine you are my personal diary. Respond naturally "
                        "in my writing style. Use at most 30 words. Match my tone "
                        "and emotional state. Avoid generic AI phrases."
                    )
                }

                response = completion.choices[0].message.content

            except Exception as e:
                print("OpenAI error:", e)
                response = (
                    "Sorry, I can't answer right now. "
                    "Please try again later."
                )

            session["conversation"].append(
                {"role": "assistant", "content": response}
            )
            session.modified = True

    return render_template(
        "write.html",
        date=date,
        response=response,
        conversation=session["conversation"]
    )
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

# Reinitialize session if reset button is pressed
@app.route("/reset", methods=["POST"])
def reset():
    session['conversation'] = []
    session.modified = True
    return redirect(url_for("write"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
