/** Подсказка при наведении на img.sign — имя файла PNG из src (например 04.01.03.png). */
(function () {
  document.querySelectorAll("img.sign").forEach(function (img) {
    var src = img.getAttribute("src") || "";
    var name = src.split("/").pop().split("\\").pop();
    if (name) {
      img.title = name;
    }
  });
})();
