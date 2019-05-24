# chess game
import sys
import logging
from inspect import getframeinfo,stack
from functools import wraps


extData={
    'functionName':"",
    'ln':""
}
fmtstr = '%(asctime)s:%(levelname)s:%(functionName)s Line:%(ln)s %(message)s'
datestr = "%m/%d/%Y %I:%M:%S %p"
logging.basicConfig(filename="chessgame_log.log",
                            level=logging.DEBUG,
                            filemode='w',
                            format=fmtstr,
                            datefmt=datestr)

def customlog(func):
    @wraps(func)
    def wrapper_log(*args,**kwargs):
        '''logging'''

        try:
            x=func(*args,**kwargs)
            extData['functionName']=getframeinfo(stack()[1][0]).function
            extData['ln']=getframeinfo(stack()[1][0]).lineno
            logging.info(f"returns {x}", extra=extData)
            return x
        except:
            logging.warning("fails to run",extra=extData)
            return x
    return wrapper_log

def help1():
    print('''This is a virtual chessboard that you can play with your friend! Follow the normal chess rules and make your move in turn. See who's better at chess!
    When it's your turn to move, 
    - After 'Move from': enter the location of the chess you want to move e.g. A1, B1
    - After 'Move to': enter the destination you want to move your chess to e.g. A2, B2
    The following rules are also applicable in this chess game:
    - en passant
    - pawn promotion
    - castling (by entering 'castling')
    - checkmate
    Game ends when king is captured. You can type 'resign' to quit at anytime. Good luck!''')

if '-h'in sys.argv or '-help' in sys.argv or '--help' in sys.argv:
    help1()

# pieces=" ".join(chr(9812+x)for x in range(12))

pindex = {'w_queen': '♕', 'w_king': '♔', 'w_rook': '♖', 'w_bishop': '♗', 'w_knight': '♘', 'w_pawn': '♙', 'b_queen': '♛',
          'b_king': '♚', 'b_rook': '♜', 'b_bishop': '♝', 'b_knight': '♞', 'b_pawn': '♟', "": ""}
loc_chess = {'A8': 'b_rook1', 'B8': 'b_knight1', 'C8': 'b_bishop1', 'D8': 'b_queen1', 'E8': 'b_king1', 'F8': 'b_bishop2',
              'G8': 'b_knight2', 'H8': 'b_rook2',
              'A7': 'b_pawn1', 'B7': 'b_pawn2', 'C7': 'b_pawn3', 'D7': 'b_pawn4', 'E7': 'b_pawn5', 'F7': 'b_pawn6',
              'G7': 'b_pawn7', 'H7': 'b_pawn8',
              'A6': "", 'B6': "", 'C6': "", 'D6': "", 'E6': "", 'F6': "", 'G6': "", 'H6': "",
              'A5': "", 'B5': "", 'C5': "", 'D5': "", 'E5': "", 'F5': "", 'G5': "", 'H5': "",
              'A4': "", 'B4': "", 'C4': "", 'D4': "", 'E4': "", 'F4': "", 'G4': "", 'H4': "",
              'A3': "", 'B3': "", 'C3': "", 'D3': "", 'E3': "", 'F3': "", 'G3': "", 'H3': "",
              'A2': 'w_pawn1', 'B2': 'w_pawn2', 'C2': 'w_pawn3', 'D2': 'w_pawn4', 'E2': 'w_pawn5', 'F2': 'w_pawn6',
              'G2': 'w_pawn7', 'H2': 'w_pawn8',
              'A1': 'w_rook1', 'B1': 'w_knight1', 'C1': 'w_bishop1', 'D1': 'w_queen1', 'E1': 'w_king1', 'F1': 'w_bishop2',
              'G1': 'w_knight2', 'H1': 'w_rook2'}
killed=[]
w_count_move=0
b_count_move=0

class Piece:
    inst_list=[]
    def __init__(self, name, position):
        self.name = name
        self.symbol=pindex[name[:-1]]
        self.position = position
        loc_chess[position] = self.name
        self.no_move = 0
        Piece.inst_list.append(self)

    def move(self, h, v, d, b,end):
        legal = True
        if h > int(self.legalmove['h']):
            legal = False
            return legal
        if abs(v) > int(self.legalmove['v']):
            legal = False
            return legal
        if d:
            if self.legalmove['d'] is False:
                legal = False
                return legal
            elif self.legalmove['d'] is True:
                if h != v:
                    legal = False
                    return legal
        return legal
    def position_update(self,end):
        global w_count_move,b_count_move
        self.no_move += 1
        self.position = end
        if self.name.startswith('w'):
            w_count_move += 1
            # print('white move: ',w_count_move)
        else:
            b_count_move += 1
            # print('black move: ',b_count_move)

    def test(self):  # test if there's any possible move by a piece:
        onestep, possible_step = [], []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                try:
                    onestep.append(chr(ord(self.position[0]) + x) + str(int(self.position[1]) + y))
                except:
                    extData['functionName'] = getframeinfo(stack()[1][0]).function
                    extData['ln'] = getframeinfo(stack()[1][0]).lineno
                    logging.debug(f'{self.name}: fail to append {self.position} to onestep', extra=extData)
                    continue
        for i in onestep:
            if i in loc_chess.keys():
                if loc_chess[i] == "" or loc_chess[i][0] != self.name[0]:  # eliminate squares occupied by pieces of same colour
                    possible_step.append(i)
        return possible_step  # return a list of all the possible steps

class King(Piece):
    legalmove = {'h': 1, 'v': 1, 'd': True, 'b': True}

class Queen(Piece):
    legalmove = {'h': 7, 'v': 7, 'd': True, 'b': True}

class Rook(Piece):
    legalmove = {'h': 7, 'v': 7, 'd': False, 'b': True}

class Bishop(Piece):
    def move(self, h, v, d, b,end):
        if h == abs(v):
            return True

    def test(self):  # test if there's any possible move by a piece:
        onestep, possible_step = [], []
        for x in [-1, 1]:
            for y in [-1, 1]:
                try:
                    onestep.append(chr(ord(self.position[0]) + x) + str(int(self.position[1]) + y))
                except:
                    extData['functionName'] = getframeinfo(stack()[1][0]).function
                    extData['ln'] = getframeinfo(stack()[1][0]).lineno
                    logging.debug(f'{self.name}: fail to append {self.position} to onestep', extra=extData)
                    continue
        for i in onestep:
            if i in loc_chess.keys():
                if loc_chess[i] == "" or loc_chess[i][0] != self.name[
                    0]:  # eliminate squares occupied by pieces of same colour
                    possible_step.append(i)
        return possible_step  # return a list of all the possible steps

class Knight(Piece):
    def move(self, h, v, d, b,end):
        legalmove = ([2, 1], [1, 2])  # h then v
        legal = False
        for i in legalmove:
            if h == i[0] and abs(v) == i[1]:
                return True
        return legal
    def test(self):  # test if there's any possible move by knight:
        return []  # return a list of all the possible steps

class Pawn(Piece):
    enpassant=""
    move_enpassant=0

    def test(self):
        onestep, possible_step = [], []
        for x in [-1, 0, 1]:
            if self.name.startswith('w'):
                for y in [0,1]:
                    onestep.append(chr(ord(self.position[0]) + x) + str(int(self.position[1]) + y))
            else:
                for y in [0,-1]:
                    onestep.append(chr(ord(self.position[0]) + x) + str(int(self.position[1]) + y))
        for i in onestep:
            if i in loc_chess.keys():
                if i[0]==self.position[0] and loc_chess[i]=="": #pawn can only move vertically if the square ahead is empty
                    possible_step.append(i)
                elif i[0]!=self.position[0] and loc_chess[i]!="":
                    if i[1] != self.position[1]: #consider diagonal square
                        if loc_chess[i][0] != self.name[0]:#pawn can only move forward diagonally if that square is not empty and occupy by opponent
                            possible_step.append(i)
                    elif i[1]==self.position[1]: #consider enpassant
                       if 'pawn' in loc_chess[i] and (i[1]=='5' or '4'):
                           possible_step.append(i)

        return possible_step  # return a list of all the possible steps

    def f_enpassant(self,enpassant,move_enpassant,w_count_move,b_count_move,end):
        if end[0]==enpassant.position[0] and (int(end[1])+1==int(enpassant.position[1]) or int(end[1])-1==int(enpassant.position[1])):
            if move_enpassant==w_count_move or move_enpassant==b_count_move: #check if it is the immediate move
                loc_chess[enpassant.position] = ""
                killed.append(enpassant)
                print('Pawn is killed by en passant')
                return True
        else:
            print('en passant not possible')
            return False

    def move(self, h, v, d, b,end):
        legal = False
        global w_count_move, b_count_move,enpassant,move_enpassant
        if loc_chess[end]=="": #pawn can move vertically if destination is empty
            if self.no_move == 0:
                if h == 0 and v <= 2 and b is False:
                    legal = True
                if v==2:
                    enpassant=self
                    move_enpassant =w_count_move+1 if self.name.startswith('w') else b_count_move+1 #timestamp the no. of move
            else:
                if h == 0 and v <= 1 and b is False:
                    legal = True
                if h==1 and v==1 and b is False:
                    legal=self.f_enpassant(enpassant,move_enpassant,w_count_move,b_count_move,end)
        else: #pawn can only capture diagonally forward one square to the left or right
            if h==1 and v==1 and b is False:
                legal=True

        return legal
    def position_update(self,end):
        super().position_update(end)
        if self.position != "":
            if self.position[1] == '8' or self.position[1]=='1':
                pawn_promote(self,end)

#instantiate the classes
king_list = [King(v,k) for k,v in loc_chess.items() if 'king' in v]
queen_list = [Queen(v,k) for k,v in loc_chess.items() if 'queen' in v]
rook_list = [Rook(v,k) for k,v in loc_chess.items() if 'rook' in v]
bishop_list = [Bishop(v,k) for k,v in loc_chess.items() if 'bishop' in v]
knight_list = [Knight(v,k) for k,v in loc_chess.items() if 'knight' in v]
pawn_list = [Pawn(v,k) for k,v in loc_chess.items() if 'pawn' in v]

def checkinstance(p): #convert the name of the pieces into instance
    for i in Piece.inst_list:
        if i.name==p:
            return i

@customlog
def printboard(loc_chess):  # print the chessboard
    board = []
    for x in range(0, 57, 8):
        y = x + 8
        board.append([i for i in [i for i in loc_chess.keys()][x:y]])
    i = 8
    for k in board:
        print('+-----' * 8, '+', sep="")
        for v in k:
            x=checkinstance(loc_chess[v])
            print('|{:^5}'.format(x.symbol if x else ""), end="")
        print('|{:^3}'.format(i), sep="")
        i = i - 1
    print('+-----' * 8, '+', sep="")
    for j in range(ord('A'), ord('I')): print(' {:^5}'.format(chr(j)), end="")
    print('\n')
    return f'board printed'

@customlog
def check_input(player):  # check if the first input is valid
    check_king = kingincheck(player)
    if check_king:
        print('king is in check! Save the king before it is captured.')
    while True:
        start = input('move from: ')
        if start[0] == " ":
            start=start.lstrip()
        if start[-1] == " ":
            start = start.rstrip()
        start=start.capitalize()
        if start in loc_chess.keys():
            p = loc_chess[start]
            if p.startswith(player) and p!="":
                x = checkinstance(p)
                if x:
                    path=x.test()  #test if there's any possible move except for knight
                    if len(path)>0 or 'knight' in x.name:
                        ck=check_move(x,start,check_king)
                        if ck:
                            return True
                    else:
                        print(f'{type(x).__name__} is stuck')
                else:
                    print('wrong move')
            else:
                print('wrong move...')
        else:
            start=start.lower()
            if start == 'castling':
                c = castling(player)
                if c:
                    print('castling done.')
                    return True
                else:
                    print('castling failed.')
                    continue
            elif start == 'resign':
                print ('alright....quit the game')
                exit()
            else:
                print('wrong character')
                continue
@customlog
def block(start, end, h, v):  # check if there's any roadblock
    x = [chr(i) for i in range(min(ord(start[0]), ord(end[0])) + 1, max(ord(start[0]), ord(end[0])))]
    if ord(end[0]) < ord(start[0]):
        x.sort(reverse=True)
    y = [str(i) for i in range(min(int(start[1]), int(end[1])) + 1, max(int(start[1]), int(end[1])))]
    if int(end[1]) < int(start[1]):
        y.sort(reverse=True)

    if int(h) != 0 and int(v) == 0:  # consider horizonal mvt
        path = [i + start[1] for i in x]
    elif int(h) == 0 and int(v) != 0:  # consider vertical mvt
        path = [start[0] + i for i in y]
    elif int(h) == int(v):  # consider diagonal mvt:
        path = [x[i] + y[i] for i in range(0, h - 1)]
    else:
        path=[]

    if len(path)>0:
        for i in path:
            if loc_chess[i] != "":
                #print(f'roadblock ahead in {i} from {start} to {end}.Steps: {path}')
                return False
        else: return path
    else:
        return end


def capture(player,start,end):
    target=loc_chess[end]
    target=checkinstance(target)
    killed.append(target)
    updateloc(player,start,end)
    target.position_update("")
    print(f'{type(player).__name__} took {type(target).__name__}.')
    if type(target).__name__=='King':
        print('Game over')
        exit()

def updateloc(player,start,end): #update the board,piece's location and no of moves
    global w_count_move, b_count_move,loc_chess
    loc_chess[start] = ""
    loc_chess[end] = player.name
    player.position_update(end)
    printboard(loc_chess)
    draw()

def draw():
    global w_count_move,b_count_move
    if w_count_move>50 or b_count_move>50: #check if there's any draw
        if len(killed)==0:
            print('exceeded 50 steps and no capture. Game over')
            exit()
        else:
            for i in Piece.inst_list:
                if 'pawn' in i.name and i.no_move>0:
                    break
            else:
                print('exceeded 50 steps and no pawn move. Game over')
                exit()


def pawn_promote(player,end): #pawn promotion
    global loc_chess
    new_class=""
    new_name=""
    while True:
        new_class = input('pawn promotion. choose queen/rook/bishop/knight:').capitalize()
        for i in (Rook,Queen,Bishop,Knight):
            if new_class == i.__name__:
                new_name = new_class.lower()
                n=2
                while True:
                    x = f'w_{new_name}{n}' if player.name.startswith('w') else f'b_{new_name}{n}'
                    if checkinstance(x):
                        n += 1
                    else:break
                x=i(x, end)  # create a new instance
                print(f'new piece {i.__name__} is created.')
                loc_chess[end] = x.name  # replace the pawn with the new piece
                player.position_update("")
                return True


def mve(player,start,end): #check if the move is valid and calculate the steps
    if end in loc_chess.keys():
            h = abs(ord(end[0]) - ord(start[0])) # check horizontal move
            v = (int(end[1]) - int(start[1])) if player.name.startswith('w') else (int(start[1]) - int(end[1]))  # check vertical move and reverse the direction for black
            if h == 0 or v == 0:  # check if it's a diagonal move
                d = False
            elif h != 0 and v != 0:
                d = True
            b = False if v >= 0 else True
            # print(f'{player.name},h:{h},v:{v},d:{d},b:{b}')
            x = player.move(h, v, d, b,end)  # validate against the legal set of moves per class
            if x:
                if 'knight' not in player.name:
                    path = block(start, end, h, v) #calculate the path. return either path or end position (if square is adjacent)
                    #print('path is ',path)
                    if path is not False:
                        return path #return the path
                    else:
                        return False
                else:
                    return player.position #knight is not blocked. return knight's position
            else:
                extData['functionName'] = getframeinfo(stack()[1][0]).function
                extData['ln'] = getframeinfo(stack()[1][0]).lineno
                logging.debug(f"set of moves not legal", extra=extData)
                return False
    else:

        extData['functionName'] = getframeinfo(stack()[1][0]).function
        extData['ln'] = getframeinfo(stack()[1][0]).lineno
        logging.debug(f"chess: {type(player).__name__} is falling off the board...", extra=extData)
        return False

def dummy(player,start,end):
    o_endpiece = loc_chess[end]
    if o_endpiece!="":
        target = checkinstance(o_endpiece)
        target.position=""
    loc_chess[start] = ""
    loc_chess[end] = player.name
    player.position=end
    # print(f'original start:{player.name}in{start}. original end:{o_endpiece}in{end}')
    # print(f'new start:{loc_chess[start]}in{start}. new end:{loc_chess[end]}in{end}')
    return o_endpiece

def reverse(start,end,o_endpiece,player):
    loc_chess[start]=player.name
    loc_chess[end]=o_endpiece
    player.position=start
    if o_endpiece!="":
        target = checkinstance(o_endpiece)
        target.position=end

def check_move(player, start,check_king):  # check if the move to destination is valid
    while True:
        end = input(f'{type(player).__name__} move to: ')
        if end[0] == " ":
            end=end.lstrip()
        if end[-1] == " ":
            end = end.rstrip()
        end=end.capitalize()
        if end =='resign':
            print('alright...quit the game.')
            exit()
        ck=mve(player, start, end) #check if the move is valid, if the path is blocked
        if ck is not False:
            if check_king: #if king is in check:
                o_endpiece=dummy(player, start, end)
                ck1 = kingincheck(player.name[0])
                reverse(start,end,o_endpiece,player)
                if ck1:
                    print('your move cannot save the king. Try again.')
                    return False
                else:
                    print('king is saved! Yeah!')

            if loc_chess[end]!="": #if destination is not empty...
                if loc_chess[end][0] == player.name[0]: #check if the player is killing his own pieces
                    print('you cannot kill yours!')
                    return False
                else:
                    capture(player,start,end)
                    return True
            else:
                updateloc(player,start,end)
                return True
        else:
            print('Cannot move this way')
            return False


def castling(player):
    rook=False
    pieces = [checkinstance('w_king1'), checkinstance('w_rook1'), checkinstance('w_rook2') if player=="w" else checkinstance('b_king1'), checkinstance('b_rook1'), checkinstance('b_rook2')]
    pieces1=[]
    if pieces[0].no_move==0: #check if the king hasn't been moved:
        #check if the king is in check
        for i in [pieces[1],pieces[2]]:
            if i not in killed and i.no_move==0: #check if the rooks are still alive and haven't been moved
                start = pieces[0].position
                end = i.position
                h = ord(end[0]) - ord(start[0])
                x = block(start, end, h, 0)  # check if the path between the king and rook is clear.
                if x is not False:
                    for j in x:
                        ck = underattack(j, player,False)  # check if any of the squares in the path is under attack by enemy
                    if ck is False: #if the square is under attack
                        pieces1.append(i.position)
        if len(pieces1)==0:
            print('castling is invalid')
            return False #no rook can be chosen
        while True: #choose the rook
            print('choose the following rook:')
            chosen = input(f'choose a rook in {pieces1}:').capitalize()
            if chosen in pieces1:
                break

        rook=checkinstance(loc_chess[chosen])
        #move the king and rook
        kmove=2 if h>0 else -2   #update king's position
        end=chr(ord(start[0]) + kmove) + str(int(start[1]))
        updateloc(pieces[0],pieces[0].position,end)
        rmove = -2 if h > 0 else 3  #update rook's position
        start=rook.position
        end = chr(ord(start[0]) + rmove) + str(int(start[1]))
        updateloc(rook,rook.position,end)
        return True

def underattack(end,player,p): #check if a square is currently under attack by enemy.
    enemy=[checkinstance(i) for i in loc_chess.values() if not i.startswith(player) and i!="" and 'king' not in i] # list of all opponents on the chessboard
    attack_paths={}
    if len(enemy)>0:
        for j in enemy:
            ck1=j.test() #check if the enemy j is blocked
            if len(ck1)>0 or 'knight' in j.name: #if j is not blocked
                ck=mve(j,j.position,end) #ck=path (list or 'end' ) or False
                if ck is not False: #valid move for the enemy
                    if p is True:  # asks for path
                        if type(ck)==str:
                            ck1=[]
                            ck1.append(str(ck))
                            ck1.append(j.position)
                            attack_paths[j] = ck1
                        else:
                            ck.append(j.position)
                            attack_paths[j]=ck
                    else:
                        print(ck)
                        attack=True
                        return attack #There is at least one enemy who can attack
                else: attack=False
            else: attack=False
        if p is True:
            return attack_paths
        else:
            return attack
    else: return False

@customlog
def kingincheck(player):
    king=checkinstance('w_king1') if player=='w' else checkinstance('b_king1')
    ck=underattack(king.position,player,True) #end: king's position. player: 'w' or 'b' True: returns attack path
    #check if the king is currently under attack by any opponent
    if ck is not False and len(ck)>0:
        print(f'way to attack the king: {ck}')
        save_a=move_king(king,player)
        if save_a is False:
            save_b=move_other_pieces(ck,player)
            if save_b is False:
                print(f'checkmate {king.symbol}. Game over! ', end="")
                print('{} won'.format('Black' if player == 'w' else 'White'))
                exit()
            else: save=True
        else: save=True
        if save:
            return True #king is in check but can be saved
    else:
        #print('king is not in check')
        return False

def move_king(king,player): #check if moving the king can save it
    king_possiblemove=king.test() #consider all possible moves by the king
    if len(king_possiblemove)>0:
        #print('king is in check. it can move to ',king_possiblemove)
        for i in king_possiblemove:
            ck1=underattack(i,player,False) #consider if each possible move can be attacked
            #print('ck1 is ', ck1)
            if ck1 is True:
                save=False
            else:
                save=True
                return save #return True when there's at least one possible move not under attack
        return save
    else: return False

def move_other_pieces(attack_paths,player): #check if moving other pieces can save the king
    if len(attack_paths)>0: #if attack_paths is not empty
        for k,v in attack_paths.items():
            opp_player = 'w' if player == 'b' else 'b'
            if 'knight' not in k.name:
                for x in v:
                    ck3 = underattack(x, opp_player, False)
                    # print('ck3 is ',ck3)
                    if ck3 is True:
                        return True   #if the opponent can be blocked
            ck2 = underattack(k.position, opp_player, False)
            if ck2 is True: #if at least one opponent can be killed
                return True
        else: return False
    else: return True

def stalemate(player): #king is not in check, all other pieces except the king is blocked but there's no legal move by the king without putting itself into check
    #check if all other pieces except the king are blocked
    pieces = [checkinstance(i) for i in loc_chess.values() if i.startswith(player) and i != ""] #list of all other pieces except the king
    for i in pieces:
        ck=i.test()
        if ck:
            return True #there's at least a piece not blocked
    #check if there's any legal move by the king
    king = checkinstance('w_king1') if player == 'w' else checkinstance('b_king1')
    ck1=move_king(king,player)
    if ck1:
        return True #there's at least one way the king can move
    else:
        print('Stalemate. Game over.')
        exit()


printboard(loc_chess)
help1()
while True:
    # white player
    print('White, please make your move.')
    check_input('w')  # return starting position and instance of piece (white)
    # black player
    print('Black, please make your move.')
    check_input('b')  # return starting position and instance of piece (black)

