let playerTurn;
let color;
let variant;
let state = {
  grid: {},
  color: color,
  variant: variant,
  rings: { white: 0, black: 0 },
  requiresSetup: true,
};

function runGame() {
  draw();

  state.variant = document.querySelector("input[name='variant']:checked").value;

  canvas.addEventListener("click", handleClick);
  if (!playerTurn) {
    state.color = "b";
    botTurn();
  } else {
    state.color = "w";
  }
}

function handleClick(e) {
  e.preventDefault();
  if (playerTurn) {
    canvas.removeEventListener("click", handleClick);
    let pos = getPosition(e);
    let hex = pixel_to_hex(pos.x, pos.y);
    if (state.requiresSetup) {
      placeMove(hex);
    } else {
      playMove(hex);
    }
  } else {
    return;
  }
}

function placeMove(hex) {
  let game = { action: hex, state: state };
  fetch("/place", { method: "POST", body: JSON.stringify(game) })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid response");
      }
      return response.json();
    })
    .then((data) => {
      game = JSON.parse(data);
      state.grid = game.state.grid;
      state.rings = game.state.rings;
      state.requiresSetup = game.state.requiresSetup;
      endTurn();
    })
    .catch((error) => {
      console.error("Invalid move", error);
      canvas.addEventListener("click", handleClick);
    });
}

function playMove(hex) {}

function endTurn() {
  updateBoard();
  checkGameOver();
  if (playerTurn) {
    playerTurn = false;
    botTurn();
  } else {
    playerTurn = true;
  }
}

function updateBoard() {
  draw();
  for (let i in state.grid) {
    let hex = grid_index[parseInt(i)];
    switch (state.grid[i]) {
      case 0:
        break;
      case 1:
        drawRing(hex, true);
        break;
      case 2:
        drawRing(hex, false);
        break;
      case 3:
        drawMarker(hex, true);
        break;
      case 4:
        drawMarker(hex, false);
    }
  }
}

function botTurn() {
  fetch("/bot", { method: "POST", body: JSON.stringify({ state: state }) })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid response");
      }
      return response.json();
    })
    .then((data) => {
      game = JSON.parse(data);
      state.grid = game.state.grid;
      state.rings = game.state.rings;
      state.requiresSetup = game.state.requiresSetup;
      canvas.addEventListener("click", handleClick);
      endTurn();
    })
    .catch((error) => {
      console.error("Invalid bot move", error);
    });
}

function checkGameOver(board) {
  // send call to api
  // if not over, return
  // if over, send winner to rematch function
  return;
}
