const ingredientInput = document.querySelector("#ingredients");
const recipeSearchForm = document.querySelector("#recipeSearchForm");
const kitchenToast = document.querySelector("#kitchenToast");
const toastBody = kitchenToast ? kitchenToast.querySelector(".toast-body") : null;

function showKitchenToast(message) {
    if (!kitchenToast || !toastBody) {
        return;
    }

    toastBody.textContent = message;
    if (window.bootstrap) {
        window.bootstrap.Toast.getOrCreateInstance(kitchenToast).show();
        return;
    }

    kitchenToast.classList.add("show");
    window.clearTimeout(kitchenToast.dataset.hideTimer);
    kitchenToast.dataset.hideTimer = window.setTimeout(() => {
        kitchenToast.classList.remove("show");
    }, 2200);
}

if (recipeSearchForm) {
    recipeSearchForm.addEventListener("submit", () => {
        const button = recipeSearchForm.querySelector(".search-submit");
        if (button) {
            button.classList.add("is-loading");
        }
    });
}

document.querySelectorAll(".copy-ingredients").forEach((button) => {
    button.addEventListener("click", async () => {
        const ingredients = button.dataset.ingredients || "";
        try {
            await navigator.clipboard.writeText(ingredients);
            showKitchenToast("Ingredients copied.");
        } catch {
            showKitchenToast(ingredients || "No ingredients to copy.");
        }
    });
});

if (window.bootstrap) {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((element) => {
        new window.bootstrap.Tooltip(element);
    });
}
