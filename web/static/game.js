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
let playHex = {};
let validDsts = [];

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
      getValidDst(hex);
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
      let game = JSON.parse(data);
      state.grid = game.state.grid;
      state.requiresSetup = game.state.requiresSetup;
      endTurn();
    })
    .catch((error) => {
      console.error("Invalid move", error);
      canvas.addEventListener("click", handleClick);
    });
}

function playMove(srcHex, dstHex) {
  let game = { action: { src: srcHex, dst: dstHex }, state: state };
  fetch("/play-dst", { method: "POST", body: JSON.stringify(game) })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid response");
      }
      return response.json();
    })
    .then((data) => {
      let game = JSON.parse(data);
      state.grid = game.state.grid;
      state.rings = game.state.rings;
      canvas.removeEventListener("click", handleDstClick);
      endTurn();
    })
    .catch((error) => {
      console.error("Invalid move", error);
    });
}

function getValidDst(hex) {
  playHex.src = hex;
  let game = { action: hex, state: state };
  fetch("/play-src", { method: "POST", body: JSON.stringify(game) })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid response");
      }
      return response.json();
    })
    .then((data) => {
      let dsts = JSON.parse(data);
      validDsts = dsts.map((i) => grid_index[parseInt(i)]);
      validDsts.forEach((hex) => drawRing(hex, state.color == "w", 0.5));
      canvas.addEventListener("click", handleDstClick);
    })
    .catch((error) => {
      console.error("Invalid source hex", error);
      canvas.addEventListener("click", handleClick);
    });
}

function handleDstClick(e) {
  e.preventDefault();
  let pos = getPosition(e);
  let hex = pixel_to_hex(pos.x, pos.y);
  // Check if hex exists in valid destinations
  if (validDsts.findIndex((dst) => dst.q == hex.q && dst.r == hex.r) != -1) {
    playMove(playHex.src, hex);
  } else if (hex.q == playHex.src.q && hex.r == playHex.src.r) {
    return;
  } else {
    canvas.removeEventListener("click", handleDstClick);
    canvas.addEventListener("click", handleClick);
    updateBoard();
    handleClick(e);
  }
}

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
      let game = JSON.parse(data);
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
