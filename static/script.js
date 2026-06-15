const savedToggle = document.querySelector("#savedToggle");
const savedRecipes = document.querySelector("#savedRecipes");
const compactToggle = document.querySelector("#compactToggle");
const recipeGrids = document.querySelectorAll(".recipe-grid");
const ingredientInput = document.querySelector("#ingredients");
const ingredientChipPreview = document.querySelector("#ingredientChipPreview");
const pantryButtons = document.querySelectorAll(".pantry-chip");
const pantryShuffle = document.querySelector("#pantryShuffle");
const clearPantry = document.querySelector("#clearPantry");
const recipeSearchForm = document.querySelector("#recipeSearchForm");
const kitchenToast = document.querySelector("#kitchenToast");
const toastBody = kitchenToast ? kitchenToast.querySelector(".toast-body") : null;

const pantrySets = [
    ["egg", "bread", "cheese"],
    ["rice", "tomato", "chicken"],
    ["pasta", "butter", "garlic"],
    ["potato", "onion", "cheese"],
];

function getIngredients() {
    if (!ingredientInput) {
        return [];
    }

    return ingredientInput.value
        .replaceAll(",", " ")
        .split(" ")
        .map((item) => item.trim().toLowerCase())
        .filter(Boolean);
}

function setIngredients(items) {
    if (!ingredientInput) {
        return;
    }

    const uniqueItems = [...new Set(items.map((item) => item.toLowerCase()))];
    ingredientInput.value = uniqueItems.join(" ");
    renderIngredientChips();
}

function renderIngredientChips() {
    if (!ingredientChipPreview) {
        return;
    }

    ingredientChipPreview.innerHTML = "";
    getIngredients().forEach((ingredient) => {
        const chip = document.createElement("span");
        chip.className = "ingredient-pill";
        chip.textContent = ingredient;
        ingredientChipPreview.appendChild(chip);
    });
}

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

function closeFallbackModal(modal) {
    modal.classList.remove("show");
    modal.setAttribute("aria-hidden", "true");
    modal.style.display = "none";
    document.body.classList.remove("modal-open");
}

function openFallbackModal(modal) {
    modal.classList.add("show");
    modal.removeAttribute("aria-hidden");
    modal.style.display = "block";
    document.body.classList.add("modal-open");
}

function setupFallbackModals() {
    if (window.bootstrap) {
        return;
    }

    document.querySelectorAll("[data-bs-toggle='modal']").forEach((button) => {
        button.addEventListener("click", () => {
            const target = document.querySelector(button.dataset.bsTarget);
            if (target) {
                openFallbackModal(target);
            }
        });
    });

    document.querySelectorAll("[data-bs-dismiss='modal']").forEach((button) => {
        button.addEventListener("click", () => {
            const modal = button.closest(".modal");
            if (modal) {
                closeFallbackModal(modal);
            }
        });
    });
}

if (savedToggle && savedRecipes) {
    savedToggle.addEventListener("change", () => {
        savedRecipes.classList.toggle("hidden-by-control", !savedToggle.checked);
        showKitchenToast(savedToggle.checked ? "Saved recipes are visible." : "Saved recipes are hidden.");
    });
}

if (compactToggle) {
    compactToggle.addEventListener("change", () => {
        recipeGrids.forEach((grid) => {
            grid.classList.toggle("compact", compactToggle.checked);
        });
        showKitchenToast(compactToggle.checked ? "Compact cards turned on." : "Compact cards turned off.");
    });
}

if (ingredientInput) {
    ingredientInput.addEventListener("input", renderIngredientChips);
    renderIngredientChips();
}

pantryButtons.forEach((button) => {
    button.addEventListener("click", () => {
        setIngredients([...getIngredients(), button.dataset.ingredient]);
        showKitchenToast(`${button.dataset.ingredient} added to the pantry.`);
    });
});

if (pantryShuffle) {
    pantryShuffle.addEventListener("click", () => {
        const randomSet = pantrySets[Math.floor(Math.random() * pantrySets.length)];
        setIngredients(randomSet);
        showKitchenToast("A surprise pantry is ready.");
    });
}

if (clearPantry) {
    clearPantry.addEventListener("click", () => {
        setIngredients([]);
        ingredientInput.focus();
        showKitchenToast("Pantry cleared.");
    });
}

if (recipeSearchForm) {
    recipeSearchForm.addEventListener("submit", () => {
        const button = recipeSearchForm.querySelector(".search-submit");
        if (button) {
            button.classList.add("is-loading");
        }
    });
}

document.querySelectorAll(".favorite-button").forEach((button) => {
    button.addEventListener("click", () => {
        button.classList.toggle("is-favorite");
        button.textContent = button.classList.contains("is-favorite") ? "Favorited" : "Favorite";
        showKitchenToast(button.classList.contains("is-favorite") ? "Recipe added to favorites." : "Recipe removed from favorites.");
    });
});

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

setupFallbackModals();
