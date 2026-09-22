const rows = document.querySelectorAll(".budget-row");
const baseOutput = document.querySelector("#base-amount");
const linesOutput = document.querySelector("#lines-budget");
const vatRateOutput = document.querySelector("#vat-rate");
const vatAmountOutput = document.querySelector("#vat-amount");
const totalAmountOutput = document.querySelector("#total-amount");
const form = document.querySelector("#budget-articles");

// Mostrar iva, base, total y lineas de forma dinámica en barra inferior.
function roundMoney(money) {
    return Math.round(Number(money) * 100) / 100;
}

function formatMoney(number) {
    return number.toLocaleString("es-ES", { style: "currency", currency: "EUR"});
}

function calculateLine(price, units, vatRate) {
    const base = roundMoney(price * units);
    const quota = roundMoney(base * (vatRate / 100));
    const total = roundMoney(base + quota);
    return {base, quota, total};
}

function calculateTotals(rows, vatRate) {
    let baseAmount = 0;
    let vatAmount = 0;
    let totalAmount = 0;
    let lines = 0;
    for (const row of rows) {
        const units = Number(row.querySelector(".units").value);
        const price = Number(row.dataset.price);
        const line = calculateLine(price, units, vatRate);
        if (units > 0) {
            lines++;
        }
        baseAmount += line.base;
        vatAmount += line.quota;
        totalAmount += line.total;
    }
    return {
        baseAmount: roundMoney(baseAmount), 
        vatAmount: roundMoney(vatAmount), 
        totalAmount: roundMoney(totalAmount), 
        lines
    }
}

function updateSummary() {
    const vatInput = document.querySelector('input[name="vat_rate"]:checked');
    const vatRate = Number(vatInput.value);
    const totals = calculateTotals(rows, vatRate);
    baseOutput.textContent = formatMoney(totals.baseAmount);
    linesOutput.textContent = totals.lines;
    vatRateOutput.textContent = vatRate;
    vatAmountOutput.textContent = formatMoney(totals.vatAmount);
    totalAmountOutput.textContent = formatMoney(totals.totalAmount);
}

// Evento que al introducir numero de articulos manualmente y
// cambiar el iva se actualiza la barra inferior.
form.addEventListener("input", updateSummary);

// Evento de sumar o restar articulos con los botones 
// y evento que actualiza barra inferior tras pulsarlos.
document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-step]");
    if (!button) return;
    const input = button.parentElement.querySelector("input[type=number]");
    if (button.dataset.step === "up") {
        input.stepUp();
    }
    else {
        input.stepDown();
    };
    updateSummary();
});

updateSummary();