from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<name>")
def wellcome(name):
    return render_template("welcome.html", name=name)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        # Just printing to console for now
        print(f"New message from {name} ({email}): {message}")
        return "Thanks for reaching out!"
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
