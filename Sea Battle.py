from random import randint
import copy

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class NearShipException(BoardException):
    def __str__(self):
        return "Рядом с подбитым кораблём не может быть ещё одного!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class ShipAtk(BoardException):
    def __str__(self):
        return "Попал"

class Board:
    def __init__(self):
        self.counter = 0

    def input_list(self,inputnumber, defcounter):
        self.field_start = []
        column = [" ", "1", "2", "3", "4", "5", "6"]
        if inputnumber==1:
            self.field_start.extend(self.line[defcounter:defcounter+6])
            self.counter+=1
            self.field_start.insert(0, column[self.counter - 1])
            return self.field_start
        else:
            self.counter=0

    def add (self):
        for i in range(1, 37):
            self.line.append("0")
        for z in range(0, 37, 6):
            self.field.append(self.input_list(1, z))
        self.input_list(0, 0)

    def Print(self):
        a=copy.deepcopy(self.field)
        for j in range (0,7):
            for i in range (0,8):
                self.field[j].insert(i*2,"|")
            print(*self.field[j])
        self.field=a

class PlaceShip(Board):
    def __init__(self,x=0,y=0,l=0,o=0):
        self.x=x
        self.y=y
        self.l=l
        self.o=o
        self.line = ["1", "2", "3", "4", "5", "6"]
        self.field = []
        self.field_start = []
        self.counter = 0
        self.busy = []
        self.busystart = []
        self.readytofight={}
    def add_ship(self,x1,y1,l,o,counter):
        len=l
        lenstart=l
        counterstrt=counter
        self.x=x1
        self.y=y1
        busyyy=self.busy
        while len != 0:
            if not self.out(self.x,self.y) and [self.x,self.y] not in self.busy:
                self.busy.append([self.x,self.y])
                self.busystart.append([self.x,self.y])
                self.x += self.direction(o,self.x, 0)
                self.y += self.direction(o,0,self.y)
                len-=1
            else:
                self.busy=busyyy
                self.busystart=[]
                self.x=randint(1,6)
                self.y=randint(1,6)
                o=randint(0,3)
                self.add_ship(self.x,self.y,lenstart,o,counterstrt)
                break
        if len == 0:

            self.readytofight[counter] = self.abrakadabra(self.busystart,lenstart)
            self.fullbusy(self.busystart)
            for [i, j] in self.busystart:
                self.field[i][j] = "■"

    def abrakadabra(self,a,b):
        abra=a[::-1]
        ll=b
        listt=[]
        for i in range(0,ll):
            listt.append(abra[i])
        return listt


    def fullbusy(self,list):
        temp = []
        for [cur_i,cur_j] in list:
            for i in range(-1,2):
                for j in range(-1,2):
                    self.busy.append([cur_i+i,cur_j+j])
        [temp.append(x) for x in self.busy if x not in temp]
        self.busy=temp

    def direction(self,o,x,y):
        direc=o
        if x == 0:
            if direc in range(2):
                return 0
            else:
                if direc == 2:
                    return -1
                else:
                    return 1
        else:
            if direc in range(2,4):
                return 0
            else:
                if direc == 0:
                    return -1
                else:
                    return 1

    def clear_board(self):
        for i in range(1,7):
            for j in range(1,7):
                self.field[i][j]="0"
        self.busy=[]

    def out(self, x,y):
        return not ((0 < x < 7) and (0 < y < 7))

    def fill_board(self):
        self.add()
        lens=[3,2,2,1,1,1]
        count=0
        for l in lens:
            try:
                self.add_ship(randint(0,6),randint(0,6),l,randint(0,3),count)
            except RecursionError:
                self.busystart=[]
                self.clear_board()
                self.readytofight = {}
                self.fill_board()
                break
            count+=1

class Game(PlaceShip):
    def __init__(self):
        self.Pl = {}
        self.Ai = {}

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
        print("-------------------")

    def start(self):
        self.loop()
        self.greet()
        self.game_process()

    def game_process(self):
        num=0
        while not self.Playerboard.readytofight == {} and not self.Aiboard.readytofight == {}:
            if num % 2 == 0:
                print("Доска игрока")
                self.Playerboard.Print()
                print("Доска для выстрелов")
                self.Playershootboard.Print()
                print("Ходит игрок, введите значения ячейки поля:")
                shot=self.inputval()
                if not type(shot) == str:
                    try:
                        r=self.playerturn(shot[0],shot[1])
                        print("-" * 40)
                        print(r)
                        print("-" * 40)
                        num+=1
                    except BoardException as e:
                        print("-" * 40)
                        print(e)
                        print("-" * 40)
                else:
                    print("-" * 40)
                    print(shot)
                    print("-" * 40)
            if num % 2 == 1:
                print("-" * 40)
                print("Ходит компьютер!!!")
                print("-" * 40)
                try:
                    r=self.Aiturn(randint(1,6),randint(1,6))
                    print(r)
                    print("-" * 40)
                    num+=1
                except BoardException as e:
                    print(e)
                    print("-" * 40)
        if num % 2 == 0:
            print("|-" * 20 + "|")
            print("Поздравляю!!! Игрок победил.")
            print("|-" * 20 + "|")
        else:
            print("|-" * 20 + "|")
            print("Попробуйте ещё раз... Компьютер победил.")
            print("|-" * 20 + "|")


    def inputval(self):
        try:
            znach = list(map(int, input().split()))
        except ValueError:
            return "Вы пытаетесь ввести не числовые значения!"
        if len(znach) < 2:
            return "Вы ввели меньше 2 значений!"
        elif len(znach) > 2:
            return "Вы ввели больше 2 значений!"
        else:
            return znach

    def loop(self):
        self.Playerboard=PlaceShip()
        self.Aiboard=PlaceShip()
        self.Playershootboard=PlaceShip()
        self.Playerboard.fill_board()
        self.Pl=copy.deepcopy(self.Playerboard.readytofight)
        self.Aiboard.fill_board()
        self.Ai=copy.deepcopy(self.Aiboard.readytofight)
        self.Playershootboard.add()

    def playerturn(self,x,y):
        if not 0 < x < 7 or not 0 < y < 7:
            raise BoardOutException()
        if self.Aiboard.field[x][y] == "T" or self.Aiboard.field[x][y] == "X":
            raise BoardUsedException()
        if self.Aiboard.field[x][y] == "*":
            raise NearShipException()
        if self.Aiboard.field[x][y] == "■":
            Shoot=self.checkAI(x,y)
            if Shoot !=100:
                self.KilledAi(Shoot)
                print("-" * 40)
                print("Корабль противника уничтожен!!!")
                print("-" * 40)
            self.Playershootboard.field[x][y] = "X"
            self.Aiboard.field[x][y] = "X"
            raise ShipAtk()
        if self.Aiboard.field[x][y] == "0":
            self.Aiboard.field[x][y] = "T"
            self.Playershootboard.field[x][y] = "T"
            return "Мимо"

    def Aiturn(self, x, y):
        if self.Playerboard.field[x][y] == "T" or self.Playerboard.field[x][y] == "X" or self.Playerboard.field[x][y] == "*":
            raise BoardUsedException()
        if self.Playerboard.field[x][y] == "■":
            Shoot = self.checkPl(x, y)
            if Shoot != 100:
                self.KilledPl(Shoot)
                print("-" * 40)
                print("Корабль противника уничтожен!!!")
                print("-" * 40)
            self.Playerboard.field[x][y] = "X"
            raise ShipAtk()
        if self.Playerboard.field[x][y] == "0":
            self.Playerboard.field[x][y] = "T"
            return "Мимо"

    def KilledAi(self,key):
        lst = self.Ai[key]
        newlst = []
        for [i, j] in lst:
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):
                    if [x, y] not in lst and 0 < x < 7 and 0 < y < 7:
                        newlst.append([x, y])
                        self.Playershootboard.field[x][y]="*"
                        self.Aiboard.field[x][y] = "*"
                    elif 0 < x < 7 and 0 < y < 7:
                        self.Playershootboard.field[x][y] = "X"
                        self.Aiboard.field[x][y] = "X"
                    else:
                        pass

    def KilledPl(self,key):
        lst = self.Pl[key]
        newlst = []
        for [i, j] in lst:
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):
                    if [x, y] not in lst and 0 < x < 7 and 0 < y < 7:
                        newlst.append([x, y])
                        self.Playerboard.field[x][y] = "*"
                    elif 0 < x < 7 and 0 < y < 7:
                        self.Playerboard.field[x][y] = "X"
                    else:
                        pass

    def checkAI(self,i,j):
        lstcount = 100
        for key in self.Aiboard.readytofight:
            x = ""
            for val in range(len(self.Aiboard.readytofight[key])):
                if self.Aiboard.readytofight[key][val] == [i, j]:
                    self.Aiboard.readytofight[key][val] = "X"
                x += str(self.Aiboard.readytofight[key][val])
            if x == "X" * len(self.Aiboard.readytofight[key]):
                lstcount=key
        if lstcount != 100:
            del self.Aiboard.readytofight[lstcount]
        return lstcount

    def checkPl(self,i,j):
        lstcount = 100
        for key in self.Playerboard.readytofight:
            x = ""
            for val in range(len(self.Playerboard.readytofight[key])):
                if self.Playerboard.readytofight[key][val] == [i, j]:
                    self.Playerboard.readytofight[key][val] = "X"
                x += str(self.Playerboard.readytofight[key][val])
            if x == "X" * len(self.Playerboard.readytofight[key]):
                lstcount=key
        if lstcount != 100:
            del self.Playerboard.readytofight[lstcount]
        return lstcount



g=Game()
g.start()





