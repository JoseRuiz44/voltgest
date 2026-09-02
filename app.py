from flask import Flask, render_template, request, redirect, url_for, session
from data import load_articles, create_article, save_articles, load_configuration, save_configuration, load_budgets, save_budgets

app = Flask(__name__)
app.secret_key = "voltgest-clave-secreta-2026"

@app.route("/")
def home():
    articles = load_articles()
    empresa = "VoltGest"
    version = "1.0"
    return render_template("home.html", empresa=empresa, version=version, articles=articles)

@app.route("/budget/client/<work_type>")
def new_budget(work_type):
    session['budget'] = {
        "work_type": work_type,
        "client": {"name": "", "address": "", "phone": ""},
        "vat_rate": 21,
        "lines": []
    }
    return render_template("budget_client.html")

@app.route("/budget/client/save", methods=["POST"])
def save_client():
    session['budget']['client']['name'] = request.form['name']
    session['budget']['client']['address'] = request.form['address']
    session['budget']['client']['phone'] = request.form['phone']
    session.modified = True
    return redirect(url_for("budget_articles"))

@app.route("/budget/articles/")
def budget_articles():
    articles = load_articles()
    return render_template("budget_articles.html", articles=articles, budget=session['budget'])

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

@app.route("/article/delete/<name>")
def delete_article(name):
    articles = load_articles()
    articles = [a for a in articles if a['name'] != name]
    save_articles(articles)
    return redirect(url_for("catalog"))

def find_article(articles, name):
    for a in articles:
        if a['name'] == name:
            return a
    return None

@app.route("/article/edit/<name>", methods=["GET", "POST"])
def edit_article(name):
    articles = load_articles()
    article = find_article(articles, name)

    if request.method == "POST":
        article['name'] = request.form['name']
        article['price'] = float(request.form['price'])
        article['scope'] = request.form['scope']
        save_articles(articles)
        return redirect(url_for("catalog"))
    return render_template("edit_article.html", article=article)

@app.route("/record")
def record():
    budgets = load_budgets()
    return render_template("record.html", budgets=budgets)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    config = load_configuration()

    if request.method == "POST":
        config['business']['name'] = request.form['name']
        config['business']['last_name'] = request.form['last_name']
        config['business']['tax_id'] = request.form['tax_id']
        config['business']['address'] = request.form['address']
        config['business']['phone'] = request.form['phone']
        config['business']['email'] = request.form['email']
        config['conditions'] = request.form['conditions']
        config['validity_days'] = request.form['validity_days']
        save_configuration(config)
        return redirect(url_for("home"))
    return render_template("settings.html", config=config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
