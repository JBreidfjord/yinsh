let playerTurn;
let color;
let variant;
let state = {
  grid: {},
  color: color,
  variant: variant,
  rings: { white: 0, black: 0 },
  requiresSetup: true,
  rows: { w: [], b: [] },
};
let playHex = {};
let validDsts = [];

function runGame() {
  draw();

  state.variant = document.querySelector("input[name='variant']:checked").value;

  canvas.addEventListener("click", handleClick);
  if (!playerTurn) {
    state.color = "b";
    state.botColor = "w";
    botTurn();
  } else {
    state.color = "w";
    state.botColor = "b";
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
      state.rows = game.state.rows;
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
  // add validation that hex is own ring
  fetch("/play-src", { method: "POST", body: JSON.stringify(game) })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Invalid response");
      }
      return response.json();
    })
    .then((data) => {
      let dsts = JSON.parse(data);
      validDsts = dsts.map((i) => gridIndex[parseInt(i)]);
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
    // Check if hex is already selected
  } else if (hex.q == playHex.src.q && hex.r == playHex.src.r) {
    return;
  } else {
    canvas.removeEventListener("click", handleDstClick);
    canvas.addEventListener("click", handleClick);
    updateBoard();
    handleClick(e);
  }
}

function handleRows() {
  if (state.rows) {
    // need to determine player order for edge cases where both sides get a row on a single turn
    if (state.rows[state.color].length !== 0) {
      canvas.addEventListener("mousemove", highlightRow);
      canvas.addEventListener("click", selectRow);
    }

    if (state.rows[state.botColor].length !== 0) {
      botRows();
    }
  }
}

function selectRow(e) {
  // add validation for overlapping rows
  let pos = getPosition(e);
  let hex = pixel_to_hex(pos.x, pos.y);
  state.rows[state.color].forEach((row) => {
    let hexRow = row.map((i) => gridIndex[parseInt(i)]);
    hexRow.forEach((h) => {
      if (h.q == hex.q && h.r == hex.r) {
        fetch("/row", {
          method: "POST",
          body: JSON.stringify({ row: hexRow, state: state }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Invalid response");
            }
            return response.json();
          })
          .then((data) => {
            let game = JSON.parse(data);
            state.grid = game.state.grid;
            state.rows = game.state.rows;
            canvas.removeEventListener("mousemove", highlightRow);
            canvas.removeEventListener("click", selectRow);
            canvas.addEventListener("mousemove", highlightRing);
            canvas.addEventListener("click", selectRing);
            updateBoard();
          })
          .catch((error) => {
            console.error("Invalid source hex", error);
          });
      }
    });
  });
}

function selectRing(e) {
  let pos = getPosition(e);
  let hex = pixel_to_hex(pos.x, pos.y);
  let hexContent =
    state.grid[invGridIndex.findIndex((h) => h.q == hex.q && h.r == hex.r)];
  if (
    (state.color == "w" && hexContent == 1) ||
    (state.color == "b" && hexContent == 2)
  ) {
    let game = { action: hex, state: state };
    fetch("/ring", { method: "POST", body: JSON.stringify(game) })
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
        state.rows = game.state.rows;
        canvas.removeEventListener("mousemove", highlightRing);
        canvas.removeEventListener("click", selectRing);
        endTurn();
      })
      .catch((error) => {
        console.error("Invalid source hex", error);
      });
  }
}

function highlightRow(e) {
  updateBoard();
  let pos = getPosition(e);
  let hex = pixel_to_hex(pos.x, pos.y);
  state.rows[state.color].forEach((row) => {
    let hexRow = row.map((i) => gridIndex[parseInt(i)]);
    hexRow.forEach((h) => {
      if (h.q == hex.q && h.r == hex.r) {
        highlightMarkers(hexRow, state.color == "w");
      }
    });
  });
}

function highlightRing(e) {
  updateBoard();
  let pos = getPosition(e);
  let hex = pixel_to_hex(pos.x, pos.y);
  let hexContent =
    state.grid[invGridIndex.findIndex((h) => h.q == hex.q && h.r == hex.r)];
  if (
    (state.color == "w" && hexContent == 1) ||
    (state.color == "b" && hexContent == 2)
  ) {
    highlightRings(hex, state.color == "w");
  }
}

function endTurn() {
  updateBoard();
  if (state.rows.w.length !== 0 || state.rows.b.length !== 0) {
    handleRows();
  } else {
    if (state.isOver) {
      getOutcome();
    }
    if (playerTurn) {
      playerTurn = false;
      botTurn();
    } else {
      playerTurn = true;
    }
  }
}

function updateBoard() {
  draw();
  for (let i in state.grid) {
    let hex = gridIndex[parseInt(i)];
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
      state.rows = game.state.rows;
      state.requiresSetup = game.state.requiresSetup;
      canvas.addEventListener("click", handleClick);
      endTurn();
    })
    .catch((error) => {
      console.error("Invalid bot move", error);
    });
}

function botRows() {
  fetch("/bot-row", { method: "POST", body: JSON.stringify({ state: state }) })
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
      state.rows = game.state.rows;
      endTurn();
    })
    .catch((error) => {
      console.error("Invalid bot move", error);
    });
}

function getOutcome() {
  // fetch outcome
  // pass winner to gameEnd()
}
