document.getElementById("select-white").onclick = function () {
  playerTurn = true;
  runGame();
};
document.getElementById("select-black").onclick = function () {
  playerTurn = false;
  runGame();
};
document.getElementById("select-random").onclick = function () {
  playerTurn = Math.random() < 0.5;
  runGame();
};

function colorSelect() {
  document.getElementById("canvas-container").style.display = "none";
  document.getElementById("rematch-container").style.display = "none";
  document.getElementById("select-container").style.display = "block";
}

function gameEnd(winner) {
  document.getElementById("rematch-container").style.display = "block";
  // display winner
  document.getElementById("rematch").onclick = function () {
    colorSelect();
  };
}
