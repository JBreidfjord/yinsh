let canvas = document.getElementById("canvas");
let w = canvas.getAttribute("width");
let h = canvas.getAttribute("height");
let size = 0.06 * w; // ((w * 0.9) / 10) * (2 / 3)

canvas.addEventListener("click", printPosition);

function lerp(a, b, t) {
  return (a + (b - a) * t).toFixed(7);
}

function hex_round(q, r, s) {
  let rq = Math.round(q);
  let rr = Math.round(r);
  let rs = Math.round(s);

  let q_diff = Math.abs(rq - q);
  let r_diff = Math.abs(rr - r);
  let s_diff = Math.abs(rs - s);

  if (q_diff > r_diff && q_diff > s_diff) {
    rq = -rr - rs;
  } else if (r_diff > s_diff) {
    rr = -rq - rs;
  } else {
    rs = -rq - rr;
  }

  return { rq, rr, rs };
}

function pixel_to_hex(x, y) {
  x = w / 2 - x;
  y = h / 2 - y;
  let q = ((2 / 3) * x) / size;
  let r = ((-1 / 3) * x + (Math.sqrt(3) / 3) * y) / size;
  return hex_round(q, r, -q - r);
}

function get_coord(col, row) {
  let tw = (col + 5) / 10;
  let th = (row - 1) / 18;

  return [lerp(w * 0.05, w * 0.95, tw), lerp(h * 0.05, h * 0.95, th)];
}

function getPosition(e) {
  let rect = e.target.getBoundingClientRect();
  let x = w - (e.clientX - rect.left); // Flip x coordinate by subtracting from width
  let y = e.clientY - rect.top;
  return { x, y };
}

function printPosition(e) {
  let position = getPosition(e);
  let hex = pixel_to_hex(position.x, position.y);
  document.getElementById("coords").value = `(${hex.rq}, ${hex.rs})`;
}

function draw() {
  if (canvas.getContext) {
    let ctx = canvas.getContext("2d");

    ctx.beginPath();
    // Vertical
    ctx.moveTo(...get_coord(-5, 7));
    ctx.lineTo(...get_coord(-5, 13));
    ctx.moveTo(...get_coord(-4, 4));
    ctx.lineTo(...get_coord(-4, 16));
    ctx.moveTo(...get_coord(-3, 3));
    ctx.lineTo(...get_coord(-3, 17));
    ctx.moveTo(...get_coord(-2, 2));
    ctx.lineTo(...get_coord(-2, 18));
    ctx.moveTo(...get_coord(-1, 1));
    ctx.lineTo(...get_coord(-1, 19));
    ctx.moveTo(...get_coord(0, 2));
    ctx.lineTo(...get_coord(0, 18));
    ctx.moveTo(...get_coord(1, 1));
    ctx.lineTo(...get_coord(1, 19));
    ctx.moveTo(...get_coord(2, 2));
    ctx.lineTo(...get_coord(2, 18));
    ctx.moveTo(...get_coord(3, 3));
    ctx.lineTo(...get_coord(3, 17));
    ctx.moveTo(...get_coord(4, 4));
    ctx.lineTo(...get_coord(4, 16));
    ctx.moveTo(...get_coord(5, 7));
    ctx.lineTo(...get_coord(5, 13));
    // SE
    ctx.moveTo(...get_coord(1, 1));
    ctx.lineTo(...get_coord(4, 4));
    ctx.moveTo(...get_coord(-1, 1));
    ctx.lineTo(...get_coord(5, 7));
    ctx.moveTo(...get_coord(-2, 2));
    ctx.lineTo(...get_coord(5, 9));
    ctx.moveTo(...get_coord(-3, 3));
    ctx.lineTo(...get_coord(5, 11));
    ctx.moveTo(...get_coord(-4, 4));
    ctx.lineTo(...get_coord(5, 13));
    ctx.moveTo(...get_coord(-4, 6));
    ctx.lineTo(...get_coord(4, 14));
    ctx.moveTo(...get_coord(-5, 7));
    ctx.lineTo(...get_coord(4, 16));
    ctx.moveTo(...get_coord(-5, 9));
    ctx.lineTo(...get_coord(3, 17));
    ctx.moveTo(...get_coord(-5, 11));
    ctx.lineTo(...get_coord(2, 18));
    ctx.moveTo(...get_coord(-5, 13));
    ctx.lineTo(...get_coord(1, 19));
    ctx.moveTo(...get_coord(-4, 16));
    ctx.lineTo(...get_coord(-1, 19));
    // SW
    ctx.moveTo(...get_coord(-1, 1));
    ctx.lineTo(...get_coord(-4, 4));
    ctx.moveTo(...get_coord(1, 1));
    ctx.lineTo(...get_coord(-5, 7));
    ctx.moveTo(...get_coord(2, 2));
    ctx.lineTo(...get_coord(-5, 9));
    ctx.moveTo(...get_coord(3, 3));
    ctx.lineTo(...get_coord(-5, 11));
    ctx.moveTo(...get_coord(4, 4));
    ctx.lineTo(...get_coord(-5, 13));
    ctx.moveTo(...get_coord(4, 6));
    ctx.lineTo(...get_coord(-4, 14));
    ctx.moveTo(...get_coord(5, 7));
    ctx.lineTo(...get_coord(-4, 16));
    ctx.moveTo(...get_coord(5, 9));
    ctx.lineTo(...get_coord(-3, 17));
    ctx.moveTo(...get_coord(5, 11));
    ctx.lineTo(...get_coord(-2, 18));
    ctx.moveTo(...get_coord(5, 13));
    ctx.lineTo(...get_coord(-1, 19));
    ctx.moveTo(...get_coord(4, 16));
    ctx.lineTo(...get_coord(1, 19));
    ctx.stroke();
  }
}
