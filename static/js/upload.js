// upload.js — drag & drop handling for the upload page

document.addEventListener("DOMContentLoaded", () => {
  const dropzone = document.getElementById("dropzone");
  const input = document.getElementById("audio_file");
  const filenameEl = document.getElementById("filename-preview");
  const pills = document.querySelectorAll(".lang-pill");
  const form = document.getElementById("upload-form");
  const submitBtn = document.getElementById("submit-btn");

  if (!dropzone || !input) return;

  dropzone.addEventListener("click", () => input.click());

  ["dragenter", "dragover"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add("dragover");
    })
  );

  ["dragleave", "drop"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.remove("dragover");
    })
  );

  dropzone.addEventListener("drop", (e) => {
    if (e.dataTransfer.files.length) {
      input.files = e.dataTransfer.files;
      showFilename();
    }
  });

  input.addEventListener("change", showFilename);

  function showFilename() {
    if (input.files.length) {
      filenameEl.textContent = "Selected: " + input.files[0].name;
      filenameEl.style.display = "block";
    }
  }

  pills.forEach((pill) => {
    pill.addEventListener("click", () => {
      pills.forEach((p) => p.classList.remove("selected"));
      pill.classList.add("selected");
    });
  });

  if (form) {
    form.addEventListener("submit", () => {
      submitBtn.disabled = true;
      submitBtn.textContent = "Processing…";
    });
  }
});
