import json
import os
import shutil

BASE_DIR = "."
DATA_PATH = os.path.join(BASE_DIR, "articles.json")
CONFIG_PATH = os.path.join(BASE_DIR, "configuration.json")
BUDGETS_PATH = os.path.join(BASE_DIR, "budgets.json")
BACKUP_ARTICLES_PATH = os.path.join(BASE_DIR, "backups", "articles", "articles.json")
BACKUP_BUDGETS_PATH = os.path.join(BASE_DIR, "backups", "budgets", "budgets.json")
PDFS_DIR = os.path.join(BASE_DIR, "pdfs")
BACKUP_CONFIG_PATH = os.path.join(BASE_DIR, "backups", "config", "configuration.json")


def set_base_dir(new_base):
    global BASE_DIR, DATA_PATH, CONFIG_PATH, BUDGETS_PATH
    global BACKUP_ARTICLES_PATH, BACKUP_BUDGETS_PATH, BACKUP_CONFIG_PATH, PDFS_DIR
    BASE_DIR = new_base
    DATA_PATH = os.path.join(BASE_DIR, "articles.json")
    CONFIG_PATH = os.path.join(BASE_DIR, "configuration.json")
    BUDGETS_PATH = os.path.join(BASE_DIR, "budgets.json")
    BACKUP_ARTICLES_PATH = os.path.join(BASE_DIR, "backups", "articles", "articles.json")
    BACKUP_BUDGETS_PATH = os.path.join(BASE_DIR, "backups", "budgets", "budgets.json")
    BACKUP_CONFIG_PATH = os.path.join(BASE_DIR, "backups", "config", "configuration.json")
    PDFS_DIR = os.path.join(BASE_DIR, "pdfs")


def backup_file(source, destination):
    if os.path.exists(source):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(source, destination)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_article(name, price, scope):
    if scope not in ["new_build", "renovation", "both"]:
        raise ValueError("Alcance del articulo no válido")
    if price <= 0:
        raise ValueError("Precio del articulo inválido")
    if not name.strip():
        raise ValueError("Nombre de artículo no puede estar vacío")
    return {
        "name": name, 
        "price": price, 
        "scope": scope
        }


def create_line(article, units, vat_included=False):
    if units < 0:
        raise ValueError("Las unidades deben ser un número positivo") 
    return {
        "article": article['name'],
        "units": units,
        "price": article['price'],
        "vat_included": vat_included
    }
    

def default_articles():
    return [
        create_article("Pica de tierra", 95, "new_build"), 
        create_article("Punto de luz", 25, "both"), 
        create_article("Desplazamiento", 40, "both"),
    ]


def save_articles(articles):
    if not isinstance(articles, list):
        return
    backup_file(DATA_PATH, BACKUP_ARTICLES_PATH)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)


def read_json_list(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError:
            pass
    return None


def load_articles():
    articles = read_json_list(DATA_PATH)
    if articles is None:
        articles = read_json_list(BACKUP_ARTICLES_PATH)
        if articles is not None:
            write_json(DATA_PATH, articles)
    if articles is None:
        articles = default_articles()
        write_json(DATA_PATH, articles)
    return articles


def default_configuration():
    return {
        "business": {
            "name": "",
            "last_name": "",
            "tax_id": "",
            "address": "",
            "phone": "",
            "email": ""
        },
        "conditions": "Documento de presupuesto, sin valor de factura. Los precios indicados son válidos durante el periodo de validez señalado; transcurrido este plazo podrán ser revisados. Los trabajos o materiales no incluidos expresamente en este presupuesto se valorarán aparte. La aceptación del presupuesto supone la conformidad con estas condiciones.",
        "validity_days": 30
    }


def save_configuration(config):
    backup_file(CONFIG_PATH, BACKUP_CONFIG_PATH)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def read_json_dict(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    return None


def load_configuration():
    config = read_json_dict(CONFIG_PATH)
    if config is None:
        config = read_json_dict(BACKUP_CONFIG_PATH)
        if config is not None:
            write_json(CONFIG_PATH, config)
    if config is None:
        config = default_configuration()
        write_json(CONFIG_PATH, config)
    return config


def load_budgets():
    budgets = read_json_list(BUDGETS_PATH)
    if budgets is None:
        budgets = read_json_list(BACKUP_BUDGETS_PATH)
        if budgets is not None:
            write_json(BUDGETS_PATH, budgets)
    if budgets is None:
        budgets = []
    return budgets


def save_budgets(budgets):
    if not isinstance(budgets, list):
        return
    backup_file(BUDGETS_PATH, BACKUP_BUDGETS_PATH)
    with open(BUDGETS_PATH, "w", encoding="utf-8") as f:
        json.dump(budgets, f, ensure_ascii=False, indent=2)

