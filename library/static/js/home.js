function loadPDF(pdfUrl) {
  const pdfViewer = document.getElementById("pdf-viewer");
  const iframe = pdfViewer.querySelector("iframe");
  iframe.src = pdfUrl;
  pdfViewer.style.display = "block";
  const bookInfoElement = document.getElementById("book-info");
  const activeBook = document.querySelector(".recent-book.active");
  const bookTitle = activeBook.querySelector("h3").textContent.trim();
  const authorName = activeBook.querySelector(".author").textContent.trim();
  const isbnText = getCurrentISBN();

  bookInfoElement.innerHTML = `<p>${bookTitle} by ${authorName}</p>`;
  bookInfoElement.innerHTML += `<p class="isbn-info">ISBN: ${isbnText}</p>`;
}

function readBook() {
  const pdfUrl = "/static/files/mech.pdf";
  loadPDF(pdfUrl);
}

function copyISBN() {
  const isbnText = getCurrentISBN();
  navigator.clipboard.writeText(isbnText).then(function () {
    alert("ISBN copied to clipboard: " + isbnText);
  });
}

function getCurrentISBN() {
  const activeBook = document.querySelector(".book-card.active");
  const isbnElement = activeBook.querySelector(".isbn");
  return isbnElement.textContent.trim();
}

function closePopover() {
  const pdfViewer = document.getElementById("pdf-viewer");
  pdfViewer.style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
  const bookCards = document.querySelectorAll(".book-card");

  bookCards.forEach(function (bookCard) {
    bookCard.addEventListener("click", function () {
      if (!bookCard.classList.contains("not-available")) {
        bookCards.forEach(function (book) {
          book.classList.remove("active");
        });

        bookCard.classList.add("active");

        readBook();
      } else {
        alert("This book is not available.");
      }
    });
  });
});
