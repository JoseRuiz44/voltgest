const shareButtons = document.querySelectorAll("[data-share-url]");

const testFile = new File([""], "prueba.pdf", { type: "application/pdf" });
const canShareFiles = navigator.canShare && navigator.canShare({ files: [testFile] });
const pdfFiles = new Map();

async function downloadPdf(url, name) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`No se pudo descargar el PDF (${response.status})`);
    }
    const blob = await response.blob();
    return new File([blob], name, { type: "application/pdf"});
}

async function prepareShareButton(button) {
    try {
        const file = await downloadPdf(button.dataset.shareUrl, button.dataset.shareName);
        pdfFiles.set(button, file);
        button.hidden = false;
    } catch (error) {
        console.error(error);
    }
}

if (canShareFiles) {
    for (const button of shareButtons) {
        prepareShareButton(button);
        button.addEventListener("click", () => sharePdf(button));
    }
}

async function sharePdf(button) {
    const file = pdfFiles.get(button);
    try {
        await navigator.share({ files: [file] });
    } catch (error) {
        if (error.name !== "AbortError") {
            console.error(error);
        }
    }
}

if (canShareFiles) {
    for (const button of shareButtons) {
        prepareShareButton(button);
    }
}
