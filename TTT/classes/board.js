class Board {
  constructor(state = ["", "", "", "", "", "", "", "", ""]) { this.state = state; }

  getFormattedBoardString() {
    let formattedString = "";
    this.state.forEach((cell, index) => {
      formattedString += cell ? ` ${cell} |` : "   |";
      if ((index + 1) % 3 === 0) {
        formattedString = formattedString.slice(0, -1);
        if (index < 8) formattedString += "\n――― ――― ―――\n";
      }
    });
    return formattedString;
  }
  printFormattedBoard() {
    console.log("%c" + this.getFormattedBoardString(), "color:#c11dd4;font-size:16px");
  }

  isEmpty() { return this.state.every(cell => !cell); }
  isFull() { return this.state.every(cell => cell); }

  insert(symbol, position) {
    if (![0,1,2,3,4,5,6,7,8].includes(position)) throw new Error("Cell index does not exist!");
    if (!["x","o"].includes(symbol)) throw new Error("The symbol can only be x or o!");
    if (this.state[position]) return false;
    this.state[position] = symbol; return true;
  }

  getAvailableMoves() {
    const moves = [];
    this.state.forEach((cell, index) => { if (!cell) moves.push(index); });
    return moves;
  }

  isTerminal() {
    if (this.isEmpty()) return false;
    if (this.state[0] && this.state[0]===this.state[1] && this.state[0]===this.state[2]) return { winner:this.state[0], direction:"H", row:1 };
    if (this.state[3] && this.state[3]===this.state[4] && this.state[3]===this.state[5]) return { winner:this.state[3], direction:"H", row:2 };
    if (this.state[6] && this.state[6]===this.state[7] && this.state[6]===this.state[8]) return { winner:this.state[6], direction:"H", row:3 };

    if (this.state[0] && this.state[0]===this.state[3] && this.state[0]===this.state[6]) return { winner:this.state[0], direction:"V", column:1 };
    if (this.state[1] && this.state[1]===this.state[4] && this.state[1]===this.state[7]) return { winner:this.state[1], direction:"V", column:2 };
    if (this.state[2] && this.state[2]===this.state[5] && this.state[2]===this.state[8]) return { winner:this.state[2], direction:"V", column:3 };

    if (this.state[0] && this.state[0]===this.state[4] && this.state[0]===this.state[8]) return { winner:this.state[0], direction:"D", diagonal:"main" };
    if (this.state[2] && this.state[2]===this.state[4] && this.state[2]===this.state[6]) return { winner:this.state[2], direction:"D", diagonal:"counter" };

    if (this.isFull()) return { winner:"draw" };
    return false;
  }
}
export default Board;
