def calculate_line(price, units, vat_rate, vat_included=False):
    if vat_rate not in [10, 21]:
        raise ValueError ("Valor de IVA inválido")
    if vat_included:
        total = round(price * units, 2)
        base = round(total / 1.10, 2) if vat_rate == 10 else round(total / 1.21, 2)
        quota = round(total - base, 2)
    else:
        base = round(price * units, 2)
        quota = round(base * 0.10, 2) if vat_rate == 10 else round(base * 0.21, 2)
        total = round(base + quota, 2)
    return {"base": base, "quota": quota, "total": total}


def calculate_totals(lines):
    base = 0
    quota = 0
    total = 0
    for line in lines:
        base += line['base']
        quota += line['quota']
        total += line['total']
    return {"base": round(base, 2), "quota": round(quota, 2), "total": round(total, 2)}


def generate_number(existing_budget, year):
    max_correlative = 0
    for budget in existing_budget:
        parts = budget['number'].split("-")
        budget_year = int(parts[1])
        budget_correlative = int(parts[2])
        if budget_year == year:
            if budget_correlative > max_correlative:
                max_correlative = budget_correlative
    max_correlative += 1
    return f"P-{year}-{max_correlative:04d}"


def ask_integer(prompt):
    while True:
        text = input(prompt)
        try:
            number = int(text)
            return number
        except ValueError:
            print("Error, introduce un entero")


def ask_number(prompt):
    while True:
        text = input(prompt)
        try:
            number = float(text)
            return number
        except ValueError:
            print("Error, introduce un decimal")

            