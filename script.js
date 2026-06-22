// script.js — shared behaviors across pages

document.addEventListener("DOMContentLoaded", () => {
  // Flip flashcards on click
  document.querySelectorAll(".flashcard").forEach((card) => {
    card.addEventListener("click", () => card.classList.toggle("flipped"));
  });

  // Quiz answer reveal
  document.querySelectorAll(".quiz-item").forEach((item) => {
    const correct = item.dataset.answer;
    item.querySelectorAll(".quiz-option").forEach((opt) => {
      opt.addEventListener("click", () => {
        item.querySelectorAll(".quiz-option").forEach((o) => o.classList.remove("correct", "incorrect"));
        if (opt.textContent.trim() === correct) {
          opt.classList.add("correct");
        } else {
          opt.classList.add("incorrect");
        }
      });
    });
  });

  // Auto-dismiss flash messages
  setTimeout(() => {
    document.querySelectorAll(".flash").forEach((f) => (f.style.opacity = "0"));
  }, 5000);
});
