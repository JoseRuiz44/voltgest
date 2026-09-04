from flask import Flask, render_template, request, redirect, url_for, session, send_file
from data import load_articles, create_article, save_articles, load_configuration, save_configuration, load_budgets, save_budgets, create_line
from calculations import calculate_line, calculate_totals, generate_number
from pdf import format_money, generate_pdf
import datetime
from io import BytesIO

app = Flask(__name__)
app.secret_key = "voltgest-clave-secreta-2026"
app.jinja_env.filters['money'] = format_money

SCOPE_ES = {"new_build": "Obra nueva", "renovation": "Reforma", "both": "Ambos"}
app.jinja_env.globals['SCOPE_ES'] = SCOPE_ES



@app.route("/")
def home():
    articles = load_articles()
    enterprise = "VoltGest"
    version = "1.0"
    return render_template("home.html", enterprise=enterprise, version=version, articles=articles)

@app.route("/budget/client/<work_type>")
def budget_client(work_type):
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

@app.route("/budget/vat_rate_articles/")
def budget_articles():
    articles = load_articles()
    return render_template("budget_articles.html", articles=articles, budget=session['budget'])

@app.route("/budget/save_articles_budget/", methods=['POST'])
def save_articles_budget():
    session['budget']['vat_rate'] = int(request.form['vat_rate'])
    session['budget']['lines'] = []

    articles = load_articles()
    for a in articles:
        campo = "units_" + a['name']
        units = int(request.form.get(campo, 0))
        if units > 0:
            session['budget']['lines'].append(create_line(a, units))
    session.modified = True
    return redirect(url_for("show_summary"))

@app.route("/budget/summary")
def show_summary():
    budget = session['budget']
    calculated_lines = [calculate_line(l['price'], l['units'], budget['vat_rate']) for l in budget['lines']]
    totals = calculate_totals(calculated_lines)
    return render_template("summary.html", budget=budget, totals=totals)

@app.route("/budget/save_budget_final", methods=["POST"])
def save_budget_final():
    budgets = load_budgets()
    budget = session['budget']
    year = datetime.date.today().year
    date = datetime.date.today().isoformat()
    budget_number = generate_number(budgets, year)
    calculated_lines = [calculate_line(l['price'], l['units'], budget['vat_rate']) for l in budget['lines']]
    totals = calculate_totals(calculated_lines)
    budget = {
        "number": budget_number,
        "date": date,
        "work_type": budget["work_type"],
        "client": budget["client"],
        "lines": budget["lines"],
        "vat_rate": budget["vat_rate"],
        "totals": totals,
    }
    budgets.append(budget)
    save_budgets(budgets)
    session.pop('budget', None)
    return redirect(url_for("preview", number=budget_number))

@app.route("/budget/preview/<number>")
def preview(number):
    return render_template("preview.html", number=number)

@app.route("/budget/pdf/<number>/<version>")
def budget_pdf(number, version):
    budgets = load_budgets()
    budget = None
    for b in budgets:
        if b['number'] == number:
            budget = b
            break
    config = load_configuration()
    internal = (version == "business")
    pdf_bytes = generate_pdf(budget, config, internal)      # ahora devuelve bytes
    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        download_name=f"{number}-{version}.pdf"
    )

@app.route("/catalog")
def catalog():
    articles = load_articles()
    return render_template("catalog.html", articles=articles)

@app.route("/catalog/new", methods=["GET", "POST"])
def new_article():
    if request.method == "POST":
        name = request.form['name'].strip()
        price = float(request.form['price'])
        scope = request.form['scope']
        articles = load_articles()
        articles.append(create_article(name, price, scope))
        save_articles(articles)
        return redirect(url_for("catalog"))
    return render_template("new_article.html")

@app.route("/catalog/delete/<name>")
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

@app.route("/catalog/edit/<name>", methods=["GET", "POST"])
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

@app.route("/budget/delete/<number>")
def delete_budget(number):
    budgets = load_budgets()
    budgets = [b for b in budgets if b['number'] != number]
    save_budgets(budgets)
    return redirect(url_for("record"))

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
        config['validity_days'] = int(request.form['validity_days'])
        save_configuration(config)
        return redirect(url_for("home"))
    return render_template("settings.html", config=config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
