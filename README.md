# ChessGame
A virtual chessboard written in python for two human players.

<div>
<img src="https://github.com/annietsang23/ChessGame/blob/master/chessgame.png" "hspace="5" width="500">
</div>

Playing instructions:

Download chessgame.py and run in console.

Follow the normal chess rules and make your move in turn. White player moves first.

When it's your turn to move, 
- After the program prints 'Move from': enter the location of the chess you want to move e.g. A1, B1
- After the program prints 'Move to': enter the destination you want to move your chess to e.g. A2, B2
- The program prints out the updated chessboard after every move.
    
The following rules/features are also applicable in this chess game:
- en passant.
- pawn promotion. The player can choose among queen/knight/rook/bishop as the piece to replace the pawn when it reaches its eighth rank.
- castling (by entering 'castling').
- checkmate (automatically checked by the program). Player must save the king first in his/her next move.
- stalemate (automatically checked by the program). While the king is not in check, all the other pieces are blocked and no legal move by the king is possible without putting itself in danger. Game is over if stalemate occurs.
- If 50 steps have been made by both players in total and no capture has been made, game is over.

Game ends when king is captured, stalemate or draw occurs. You can type 'resign' to quit at anytime.

Implementation:
- OOP principles are heavily adopted with 2 levels of inheritance (Chess piece as superclass and different types of chess pieces such as queen, king etc. as subclasses). While all chess pieces inherited the name, symbol and position properties from superclass, they have different set of legal movements at subclass level.

- Checkmate condition is automatically checked by my program via the following steps:
  - After every piece movement, the program calculates the range of next legal movement potentially made by all opponent pieces and checks if the king is under attack.
  - If the king is under attack, the program checks if there's a way to save the king by moving the king, moving any piece to block the attack path, or kill the opponent piece which is attacking the king.
  - If there's a possible way to save the king from danger, the program prints 'king is in check! Save the king before it is captured.'
  - If there's no possible way to save the king, the program prints 'checkmate king. Game over!'

- Stalemate condition is automatically determined by my program via the following steps:
  - The program checks if all pieces except the king are blocked
  - If the above occurs and no possible legal move can be made by the king without putting itself within the attack range of opponent pieces, stalemate occurs. The program prints 'Stalemate. Game over'.

- A logging file named 'chessgame_log.log' will be automatically created in the same directory as the chessgame.py file to track any illegal moves or attack on the king(s) during the game. It is implemented using python function decorators (The logging function is called 'customlog').




