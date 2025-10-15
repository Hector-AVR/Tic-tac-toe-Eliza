//Helpers
export function hasClass(el, className) {
  if (el.classList) return el.classList.contains(className);
  return !!el.className.match(new RegExp("(\\s|^)" + className + "(\\s|$)"));
}
export function addClass(el, className) {
  if (el.classList) el.classList.add(className);
  else if (!hasClass(el, className)) el.className += " " + className;
}
export function removeClass(el, className) {
  if (el.classList) el.classList.remove(className);
  else if (hasClass(el, className)) {
    const reg = new RegExp("(\\s|^)" + className + "(\\s|$)");
    el.className = el.className.replace(reg, " ");
  }
}
// Dibuja la línea ganadora
export function drawWinningLine(statusObject) {
  if (!statusObject) return;
  const { winner, direction, row, column, diagonal } = statusObject;
  if (winner === "draw") return;
  const board = document.getElementById("board");
  addClass(board, `${direction.toLowerCase()}-${row || column || diagonal}`);
  setTimeout(() => addClass(board, "fullLine"), 50);
}
