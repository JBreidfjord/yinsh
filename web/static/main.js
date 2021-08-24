document.getElementById("select-white").onclick = function () {
  draw();
  // setTimeout required to force DOM update
  setTimeout(function () {
    runGame(true);
  }, 0);
};
document.getElementById("select-black").onclick = function () {
  draw();
  setTimeout(function () {
    runGame(false);
  }, 0);
};
document.getElementById("select-random").onclick = function () {
  draw();
  setTimeout(function () {
    runGame(Math.random() < 0.5);
  }, 0);
};

function colorSelect() {
  document.getElementById("canvas-container").style.display = "none";
  document.getElementById("rematch-container").style.display = "none";
  document.getElementById("select-container").style.display = "block";
}

function gameEnd(winner) {
  document.getElementById("rematch-container").style.display = "block";
  document.getElementById("rematch").onclick = function () {
    colorSelect();
  };
}
