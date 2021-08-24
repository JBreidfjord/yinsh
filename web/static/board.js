const canvas = document.getElementById("canvas");
const w = canvas.width;
const h = canvas.height;
const size = 0.06 * w; // ((w * 0.9) / 10) * (2 / 3)

function draw() {
  document.getElementById("select-container").style.display = "none";
  document.getElementById("canvas-container").style.display = "block";
  canvas.addEventListener("mousemove", printPosition);
  if (canvas.getContext) {
    let ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

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

function get_coord(col, row) {
  let tw = (col + 5) / 10;
  let th = (row - 1) / 18;

  return [lerp(w * 0.05, w * 0.95, tw), lerp(h * 0.05, h * 0.95, th)];
}

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

  return { rq, rs };
}

function pixel_to_hex(x, y) {
  x = w / 2 - x;
  y = h / 2 - y;
  let q = ((2 / 3) * x) / size;
  let r = ((-1 / 3) * x + (Math.sqrt(3) / 3) * y) / size;
  return hex_round(q, r, -q - r);
}

function hex_to_pixel(q, r) {
  let x = size * ((3 / 2) * q);
  let y = size * ((Math.sqrt(3) / 2) * q + Math.sqrt(3) * r);
  x = w / 2 - x;
  y = h / 2 - y;
  return { x, y };
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
  if (
    Math.abs(hex.rq) + Math.abs(hex.rs) < 10 &&
    Math.abs(hex.rq) <= 5 &&
    Math.abs(hex.rs) <= 5
  ) {
    document.getElementById("coords").value = `(${hex.rq}, ${hex.rs})`;
  } else {
    document.getElementById("coords").value = "";
  }
}
