from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from data import load_articles, create_article, save_articles, load_configuration, save_configuration, load_budgets, save_budgets, create_line
from calculations import calculate_line, calculate_totals, generate_number
from pdf import format_money, generate_pdf
import datetime
from io import BytesIO

app = Flask(__name__)
app.secret_key = "voltgest-clave-secreta-2026"
app.jinja_env.globals['money'] = format_money

SCOPE_ES = {"new_build": "Obra nueva", "renovation": "Reforma", "both": "Ambos"}
app.jinja_env.globals['SCOPE_ES'] = SCOPE_ES

@app.route("/")
def home():
    session.pop('budget', None)
    articles = load_articles()
    enterprise = "VoltGest"
    version = "1.0"
    return render_template("home.html", enterprise=enterprise, version=version, articles=articles)

@app.route("/budget/client/<work_type>")
def budget_client(work_type):
    if 'budget' not in session:
        session['budget'] = {
            "work_type": work_type,
            "client": {"name": "", "address": "", "phone": ""},
            "vat_rate": 21,
            "lines": []
        }
    return render_template("budget_client.html")

@app.route("/budget/client/save", methods=["POST"])
def save_client():
    if 'budget' not in session:
        flash("Primero inicia un presupuesto")
        return redirect(url_for("home"))
    session['budget']['client']['name'] = request.form['name']
    session['budget']['client']['address'] = request.form['address']
    session['budget']['client']['phone'] = request.form['phone']
    session.modified = True
    return redirect(url_for("budget_articles"))

@app.route("/budget/vat_rate_articles/")
def budget_articles():
    if 'budget' not in session:
        flash("Primero inicia un presupuesto")
        return redirect(url_for("home"))
    articles = load_articles()
    units_by_article = {line['article']: line['units'] for line in session['budget']['lines']}
    return render_template("budget_articles.html", articles=articles, budget=session['budget'], units_by_article=units_by_article)

@app.route("/budget/save_articles_budget/", methods=['POST'])
def save_articles_budget():
    if 'budget' not in session:
        flash("Primero inicia un presupuesto")
        return redirect(url_for("home"))
    session['budget']['vat_rate'] = int(request.form['vat_rate'])
    session['budget']['lines'] = []
    articles = load_articles()
    for a in articles:
        campo = "units_" + a['name']
        units = int(request.form.get(campo, 0))
        if units > 0:
            session['budget']['lines'].append(create_line(a, units))
    session.modified = True
    if not session['budget']['lines']:
        flash("Añade al menos un artículo al presupuesto")
        return redirect(url_for("budget_articles"))
    return redirect(url_for("show_summary"))

@app.route("/budget/summary")
def show_summary():
    if 'budget' not in session:
        flash("Primero inicia un presupuesto")
        return redirect(url_for("home"))
    budget = session['budget']
    calculated_lines = [calculate_line(l['price'], l['units'], budget['vat_rate']) for l in budget['lines']]
    totals = calculate_totals(calculated_lines)
    return render_template("summary.html", budget=budget, totals=totals)

@app.route("/budget/save_budget_final", methods=["POST"])
def save_budget_final():
    if 'budget' not in session:
        flash("Primero inicia un presupuesto")
        return redirect(url_for("home"))
    budget = session['budget']
    if not budget['lines']:
        flash("Añade al menos un artículo al presupuesto")
        return redirect(url_for("budget_articles"))
    budgets = load_budgets()
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
    flash(f"Presupuesto '{budget['number']}' creado correctamente")
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
    session.pop('budget', None)
    articles = load_articles()
    return render_template("catalog.html", articles=articles)

@app.route("/catalog/new", methods=["GET", "POST"])
def new_article():
    if request.method == "POST":
        name = request.form['name'].strip()
        scope = request.form['scope']
        price_text = request.form['price']
        
        try:
            price = float(price_text.replace(",", "."))
        except ValueError:
            flash("Introduce un numero en el campo precio")
            return render_template("new_article.html", name=name, price=price_text, scope=scope)
        
        if not name:
            flash("El nombre del artículo no puede estar vacío")
            return render_template("new_article.html", name=name, price=price_text, scope=scope)

        if price <= 0:
            flash("El precio debe ser mayor que 0")
            return render_template("new_article.html", name=name, price=price_text, scope=scope)
        
        articles = load_articles()
        for article in articles:
            if name.lower() == article['name'].lower():
                flash("El nombre del artículo ya existe")
                return render_template("new_article.html", name=name, price=price_text, scope=scope)

        articles.append(create_article(name, price, scope))
        save_articles(articles)
        flash(f"Artículo '{name}' creado correctamente")
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
        if a['name'].lower() == name.lower():
            return a
    return None

@app.route("/catalog/edit/<name>", methods=["GET", "POST"])
def edit_article(name):
    articles = load_articles()
    current_article = find_article(articles, name)
    if request.method == "POST":
        current_name = request.form['name'].strip()
        current_scope = request.form['scope']
        price_text = request.form['price']

        try:
            current_price = float(price_text.replace(",", "."))
        except ValueError:
            flash("Introduce un numero en el campo precio")
            return render_template("edit_article.html", article=current_article)
        
        if not current_name:
            flash("El nombre del artículo no puede estar vacío")
            return render_template("edit_article.html", article=current_article)
        
        if current_price <= 0:
            flash("El precio debe ser mayor que 0")
            return render_template("edit_article.html", article=current_article)
        
        for a in articles:
            if a is current_article:
                continue
            if current_name.lower() == a['name'].lower():
                flash("El nombre del artículo ya existe")
                return render_template("edit_article.html", article=current_article)

        current_article['name'] = current_name
        current_article['price'] = current_price
        current_article['scope'] = current_scope

        save_articles(articles)
        flash(f"Artículo '{current_article['name']}' editado correctamente")
        return redirect(url_for("catalog"))
    return render_template("edit_article.html", article=current_article)

@app.route("/record")
def record():
    session.pop('budget', None)
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
    session.pop('budget', None)
    config = load_configuration()
    if request.method == "POST":
        name = request.form['name']
        last_name = request.form['last_name']
        tax_id = request.form['tax_id']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        validity_days = request.form['validity_days']
        conditions = request.form['conditions']

        try:
            validity_days = int(validity_days)
        except ValueError:
            flash("El campo 'Validez' solo admite números enteros")
            return render_template("settings.html", config=config)

        config['business']['name'] = name
        config['business']['last_name'] = last_name
        config['business']['tax_id'] = tax_id
        config['business']['address'] = address
        config['business']['phone'] = phone
        config['business']['email'] = email
        config['validity_days'] = validity_days
        config['conditions'] = conditions
        save_configuration(config)
        flash("Ajustes guardados correctamente")
        return redirect(url_for("home"))
    return render_template("settings.html", config=config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
