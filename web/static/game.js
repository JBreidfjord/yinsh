function runGame(playerTurn) {
  if (playerTurn) {
    canvas.addEventListener("click", handleClick);
  }

  checkGameOver();
}

function handleClick(e) {}

function checkGameOver(board) {
  // send call to api
  // if not over, return
  // if over, send winner to rematch function
  return;
}
