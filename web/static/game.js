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
    handleAction(hex);
  } else {
    return;
  }
}

function handleAction(hex) {
  let valid;
  if (state.requiresSetup) {
    valid = placeMove(hex);
  } else {
    valid = playMove(hex);
  }
  if (valid) {
    playerTurn = false;
    botTurn();
  } else {
    canvas.addEventListener("click", handleClick);
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
      data = JSON.parse(data);
      console.log(data);
      console.log(state);
      state.grid = data.state.grid;
      state.rings = data.state.rings;
      state.requiresSetup = data.state.requiresSetup;
      updateBoard();
    })
    .catch((error) => {
      console.error("Invalid move", error);
    });
}

function playMove(hex) {}

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
  // bot action
  playerTurn = true;
  canvas.addEventListener("click", handleClick);
}

function checkGameOver(board) {
  // send call to api
  // if not over, return
  // if over, send winner to rematch function
  return;
}

// JSON Legend:
// Empty: 0
// White Ring: 1
// Black Ring: 2
// White Marker: 3
// Black Marker: 4
