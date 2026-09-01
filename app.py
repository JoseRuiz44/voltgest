from flask import Flask, render_template, request, redirect, url_for
from data import load_articles, create_article, save_articles

app = Flask(__name__)

@app.route("/")
def home():
    articles = load_articles()
    empresa = "VoltGest"
    version = "1.0"
    return render_template("home.html", empresa=empresa, version=version, articles=articles)

@app.route("/catalog")
def catalog():
    articles = load_articles()
    return render_template("catalog.html", articles=articles)

@app.route("/article/new", methods=["GET", "POST"])
def new_article():
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        scope = request.form['scope']
        articles = load_articles()
        articles.append(create_article(name, price, scope))
        save_articles(articles)
        return redirect(url_for("catalog"))
    return render_template("new_article.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
