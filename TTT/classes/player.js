import Board from "./board.js";

export default class Player {
  constructor(maxDepth = -1) {
    this.maxDepth = maxDepth;
    this.nodesMap = new Map();
  }

  getBestMove(board, maximizing = true, callback = () => {}, depth = 0) {
    if (depth === 0) this.nodesMap.clear();

    const terminal = board.isTerminal();
    if (terminal || (this.maxDepth !== -1 && depth === this.maxDepth)) {
      if (terminal && terminal.winner === "x") return 100 - depth;
      if (terminal && terminal.winner === "o") return -100 + depth;
      return 0;
    }

    if (maximizing) {
      let best = -100;
      board.getAvailableMoves().forEach(index => {
        const child = new Board([...board.state]);
        child.insert("x", index);
        const nodeValue = this.getBestMove(child, false, callback, depth + 1);
        best = Math.max(best, nodeValue);
        if (depth === 0) {
          const moves = this.nodesMap.has(nodeValue)
            ? `${this.nodesMap.get(nodeValue)},${index}` : index;
          this.nodesMap.set(nodeValue, moves);
        }
      });
      if (depth === 0) {
        let returnValue;
        if (typeof this.nodesMap.get(best) === "string") {
          const arr = this.nodesMap.get(best).split(",");
          returnValue = arr[Math.floor(Math.random() * arr.length)];
        } else returnValue = this.nodesMap.get(best);
        callback(returnValue);
        return returnValue;
      }
      return best;
    } else {
      let best = 100;
      board.getAvailableMoves().forEach(index => {
        const child = new Board([...board.state]);
        child.insert("o", index);
        const nodeValue = this.getBestMove(child, true, callback, depth + 1);
        best = Math.min(best, nodeValue);
        if (depth === 0) {
          const moves = this.nodesMap.has(nodeValue)
            ? `${this.nodesMap.get(nodeValue)},${index}` : index;
          this.nodesMap.set(nodeValue, moves);
        }
      });
      if (depth === 0) {
        let returnValue;
        if (typeof this.nodesMap.get(best) === "string") {
          const arr = this.nodesMap.get(best).split(",");
          returnValue = arr[Math.floor(Math.random() * arr.length)];
        } else returnValue = this.nodesMap.get(best);
        callback(returnValue);
        return returnValue;
      }
      return best;
    }
  }
}
