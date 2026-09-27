const dialog = document.querySelector(".confirm-dialog");
const question = dialog.querySelector(".confirm-question");
const acceptButton = dialog.querySelector(".confirm-accept");
const confirmForm = dialog.querySelector("form");

document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-confirm-url]");
    if (!trigger) return;

    question.textContent = trigger.dataset.confirmText;
    acceptButton.textContent = trigger.dataset.confirmAction;
    confirmForm.action = trigger.dataset.confirmUrl;
    dialog.showModal();
});
