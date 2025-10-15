import Board from "./classes/board.js";
import Player from "./classes/player.js";
import { drawWinningLine, hasClass, addClass } from "./helpers.js";

function newGame(depth = -1, startingPlayer = 1) {
  const player = new Player(parseInt(depth));
  const board = new Board(["", "", "", "", "", "", "", "", ""]);

  const boardDIV = document.getElementById("board");
  boardDIV.className = "";
  boardDIV.innerHTML = `<div class="cells-wrap">
      <button class="cell-0"></button>
      <button class="cell-1"></button>
      <button class="cell-2"></button>
      <button class="cell-3"></button>
      <button class="cell-4"></button>
      <button class="cell-5"></button>
      <button class="cell-6"></button>
      <button class="cell-7"></button>
      <button class="cell-8"></button>
    </div>`;

  const htmlCells = [...boardDIV.querySelector(".cells-wrap").children];

  const starting = parseInt(startingPlayer);   // 1 humano, 0 compu
  const maximizing = starting;                 // humano 'x' si maximizing = 1
  let playerTurn = starting;

  // Si inicia la compu, juega al centro/esquinas
  if (!starting) {
    const centerAndCorners = [0, 2, 4, 6, 8];
    const firstChoice = centerAndCorners[Math.floor(Math.random() * centerAndCorners.length)];
    const symbol = !maximizing ? "x" : "o"; // si humano NO es max (0), compu es 'x'
    board.insert(symbol, firstChoice);
    addClass(htmlCells[firstChoice], symbol);
    playerTurn = 1;
  }

  // Clicks del humano
  board.state.forEach((cell, index) => {
    htmlCells[index].addEventListener("click", () => {
      if (
        hasClass(htmlCells[index], "x") ||
        hasClass(htmlCells[index], "o") ||
        board.isTerminal() || !playerTurn
      ) return false;

      const symbol = maximizing ? "x" : "o";
      board.insert(symbol, index);
      addClass(htmlCells[index], symbol);

      if (board.isTerminal()) drawWinningLine(board.isTerminal());

      playerTurn = 0;

      // Movimiento de la compu
      player.getBestMove(board, !maximizing, best => {
        const compSymbol = !maximizing ? "x" : "o";
        board.insert(compSymbol, parseInt(best));
        addClass(htmlCells[best], compSymbol);
        if (board.isTerminal()) drawWinningLine(board.isTerminal());
        playerTurn = 1;
      });
    }, false);

    if (cell) addClass(htmlCells[index], cell);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // tablero visible desde el arranque
  newGame(-1, 1);

  document.getElementById("newGame").addEventListener("click", () => {
    const starting = document.getElementById("starting").value;
    const depth = document.getElementById("depth").value;
    newGame(depth, starting);
  });
});
