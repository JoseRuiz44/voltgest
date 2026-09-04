from fpdf import FPDF
import datetime
import os

# --- Paleta de colores ---
FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts")
COLOR_MAIN = (11, 85, 99)      # Azul corporativo
COLOR_TEXT_MAIN = (26, 26, 26)   # Gris oscuro para textos principales
COLOR_TEXT_MUTED = (102, 102, 102) # Gris medio para etiquetas/direcciones
COLOR_TEXT_HEADER = (153, 153, 153) # Gris claro para Emisor/Destinatario y datos cabecera
COLOR_ROW_ALT = (245, 247, 248)   # Gris-azul para filas alternas
COLOR_WHITE = (255, 255, 255)

# Funciones
def write_text(pdf, x, y, text, width=0, size=10, bold=False, align="L", color=COLOR_TEXT_MAIN):
    style = "B" if bold else ""
    pdf.set_font("dejavu", size=size, style=style)
    pdf.set_text_color(*color)
    pdf.set_xy(x, y)
    pdf.cell(width, 5, text, align=align)


def draw_line(pdf, x1, y1, x2, y2, color=COLOR_MAIN):
    pdf.set_draw_color(*color)
    pdf.line(x1, y1, x2, y2)


def fill_rect(pdf, x, y, width, height, color):
    pdf.set_fill_color(*color)
    pdf.rect(x, y, width, height, "F")


def format_money(amount):
    text = f"{amount:,.2f}"
    text = text.replace(",", "x").replace(".", ",").replace("x", ".")
    return f"{text} €"

def generate_pdf(budget, config, internal):
    # --- Generación del PDF ---
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("dejavu", "", os.path.join(FONTS_DIR, "DejaVuSans.ttf"))
    pdf.add_font("dejavu", "B", os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf"))

    # Cabecera Izquierda
    write_text(pdf, 20, 20, "PRESUPUESTO", size=24, bold=True)
    copy_label = "COPIA EMPRESA" if internal else "COPIA CLIENTE"
    write_text(pdf, 20, 28, f"{copy_label}", size=9, bold=True, color=COLOR_MAIN)

    # Cabecera Derecha (Metadatos)
    write_text(pdf, 20, 18, "Nº Presupuesto", width=130, size=9, align="R", color=COLOR_TEXT_HEADER)
    write_text(pdf, 20, 18, f"{budget['number']}", width=170, size=9, bold=True, align="R")
    
    write_text(pdf, 20, 23, "Fecha", width=130, size=9, align="R", color=COLOR_TEXT_HEADER)
    date = datetime.date.fromisoformat(budget['date']).strftime("%d/%m/%Y")
    write_text(pdf, 20, 23, f"{date}", width=170, size=9, bold=True, align="R")
    
    write_text(pdf, 20, 28, "Validez", width=130, size=9, align="R", color=COLOR_TEXT_HEADER)
    write_text(pdf, 20, 28, f"{config['validity_days']} días", width=170, size=9, bold=True, align="R")

    draw_line(pdf, 20, 38, 190, 38)

    # Bloque Emisor
    write_text(pdf, 20, 42, "EMISOR", bold=True, color=COLOR_TEXT_HEADER, size=9)
    write_text(pdf, 20, 49, f"{config['business']['name']} {config['business']['last_name']}", bold=True, size=11)
    write_text(pdf, 20, 54, f"{config['business']['tax_id']}", color=COLOR_TEXT_MUTED, size=9)
    write_text(pdf, 20, 59, f"{config['business']['address']}", color=COLOR_TEXT_MUTED, size=9)
    write_text(pdf, 20, 64, f"{config['business']['phone']} - {config['business']['email']}", color=COLOR_TEXT_MUTED, size=9)

    # Bloque Destinatario
    write_text(pdf, 105, 42, "DESTINATARIO", bold=True, color=COLOR_TEXT_HEADER, size=9)
    write_text(pdf, 105, 49, f"{budget['client']['name']}", bold=True, size=11)
    write_text(pdf, 105, 54, f"{budget['client']['address']}", color=COLOR_TEXT_MUTED, size=9)
    write_text(pdf, 105, 59, f"{budget['client']['phone']}", color=COLOR_TEXT_MUTED, size=9)
    work_type_pdf = "Obra nueva" if budget['work_type'] == "new_build" else "Reforma"
    write_text(pdf, 105, 64, f"{work_type_pdf}", color=COLOR_TEXT_MUTED, size=9)

    # --- TABLA DE ARTÍCULOS ---
    if internal:
        # Encabezado company_version -------------------------------
        fill_rect(pdf, 20, 76, 170, 8, COLOR_MAIN)
        write_text(pdf, 20, 78, "CONCEPTO", bold=True, color=COLOR_WHITE)
        write_text(pdf, 20, 78, "UDS", width=90, align="R", bold=True, color=COLOR_WHITE)
        write_text(pdf, 20, 78, "PRECIO", width=130, align="R", bold=True, color=COLOR_WHITE)
        write_text(pdf, 20, 78, "IMPORTE", width=170, align="R", bold=True, color=COLOR_WHITE)

        # Cuerpo de la tabla
        current_y = 84
        color = COLOR_ROW_ALT
        for budget_line in budget['lines']:
            fill_rect(pdf, 20, current_y, 170, 8, color)
            write_text(pdf, 20, (current_y+2), f"{budget_line['article']}")
            write_text(pdf, 20, (current_y+2), f"{budget_line['units']}", width=90, align="R")
            write_text(pdf, 20, (current_y+2), f"{format_money(budget_line['price'])}", width=130, color=COLOR_TEXT_MUTED, align="R")
            write_text(pdf, 20, (current_y+2), f"{format_money(budget_line['price']* budget_line['units'])}", width=170, align="R")
            current_y += 8
            if color == COLOR_WHITE:
                color = COLOR_ROW_ALT
            else:
                color = COLOR_WHITE
        draw_line(pdf, 20, current_y, 190, current_y)
    else:
        # Encabezado client_version -----------------------------
        fill_rect(pdf, 20, 76, 170, 8, COLOR_MAIN)
        write_text(pdf, 20, 78, "CONCEPTO", bold=True, color=COLOR_WHITE)
        write_text(pdf, 20, 78, "UDS", width=130, align="R", bold=True, color=COLOR_WHITE)
        write_text(pdf, 20, 78, "IMPORTE", width=170, align="R", bold=True, color=COLOR_WHITE)


        # Cuerpo de la tabla
        current_y = 84
        color = COLOR_ROW_ALT
        for budget_line in budget['lines']:
            fill_rect(pdf, 20, current_y, 170, 8, color)
            write_text(pdf, 20, (current_y+2), f"{budget_line['article']}")
            write_text(pdf, 20, (current_y+2), f"{budget_line['units']}", width=130, align="R")
            current_y += 8
            if color == COLOR_WHITE:
                color = COLOR_ROW_ALT
            else:
                color = COLOR_WHITE
        draw_line(pdf, 20, current_y, 190, current_y)

    # Base, IVA, total
    current_y += 5
    write_text(pdf, 20, (current_y), "Base imponible", width=130, align="R", color=COLOR_TEXT_MUTED, size=9)
    write_text(pdf, 20, (current_y), f"{format_money(budget['totals']['base'])}", width=170, align="R", size=9)

    current_y += 5
    write_text(pdf, 20, (current_y), f"IVA ({budget['vat_rate']}%)", width=130, align="R", color=COLOR_TEXT_MUTED, size=9)
    write_text(pdf, 20, (current_y), f"{format_money(budget['totals']['quota'])}", width=170, align="R", size=9)

    current_y += 7
    draw_line(pdf, 145, current_y, 190, current_y)

    current_y += 2
    write_text(pdf, 20, (current_y), "TOTAL", width=130, align="R", bold=True, color=COLOR_MAIN, size=11)
    write_text(pdf, 20, (current_y), f"{format_money(budget['totals']['total'])}", width=170, align="R", bold=True, size=11)

    # Parrafo condiciones
    draw_line(pdf, 20, 254, 190, 254)
    pdf.set_font("dejavu", size=8)
    pdf.set_text_color(*COLOR_TEXT_MUTED)
    pdf.set_xy(20, 255)
    pdf.multi_cell(170, 4, config['conditions'])

    # Mensaje de generacion y numero de pagina
    write_text(pdf, 20, 272, "Generado por VoltGest", color=COLOR_TEXT_HEADER, size=8)
    write_text(pdf, 20, 272, "Página 1 de 1", width=170, align="R", color=COLOR_TEXT_HEADER, size=8)

    return bytes(pdf.output())

def generate_both(budget, config):
    generate_pdf(budget, config, internal=True)
    generate_pdf(budget, config, internal=False)
