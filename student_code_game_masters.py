from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        tuple_lst = []

        tmp_lst = []
        for i in range(3):
            ask1 = parse_input("fact: (on ?X peg" + str(i+1))
            ans = self.kb.kb_ask(ask1)
            if ans:
                for binding in ans:
                    disk_num = int(binding.bindings_dict["?X"][-1])
                    tmp_lst.append(disk_num)
            tmp_lst.sort()
            mytuple = tuple(tmp_lst) 
            tmp_lst = []
            tuple_lst.append(mytuple)
        return tuple(tuple_lst)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        
        if not self.isMovableLegal(movable_statement):
            return False 

        # Get the elements

        disk1 = movable_statement.terms[0].term.element
        peg1 = movable_statement.terms[1].term.element
        peg2 = movable_statement.terms[2].term.element


        # Switch what is "on" 

        r1 = parse_input("fact: (on " + disk1 + " " + peg1 + ")")
        self.kb.kb_retract(r1)
        assert1 = parse_input("fact: (on " + disk1 + " " + peg2 + ")")
        self.kb.kb_assert(assert1)


        # Change start peg facts 
        r2 = parse_input("fact: (top " + disk1 + " " + peg1 + ")")
        self.kb.kb_retract(r2)

        ask1 = parse_input("fact: (on ?X " + peg1 + ")")
        disks_under = self.kb.kb_ask(ask1)

        if not disks_under:
            assert1 = parse_input("fact: (empty " + peg1 + ")")
            self.kb.kb_assert(assert1)
        else:
            # find top most disk (least in value, smallest)
            smallest_disk = disks_under[0].bindings_dict["?X"]
            for each_disk in disks_under: 
                d = each_disk.bindings_dict["?X"]
                if int(d[-1]) < int(smallest_disk[-1]):
                    smallest_disk = d 
            assert1 = parse_input("fact: (top " + smallest_disk + " " + peg1 + ")")
            self.kb.kb_assert(assert1)


        # If destination is empty, retract that fact

        r2 = parse_input("fact: (empty " + peg2 + ")")
        self.kb.kb_retract(r2)

        # If destination has a disk, retract that top

        ask1 = parse_input("fact: (top ?X " + peg2 + ")")
        previous_top = self.kb.kb_ask(ask1)
        if previous_top:
            previous_top = previous_top[0].bindings_dict["?X"]
            r3 = parse_input("fact: (top " + previous_top + " " + peg2 + ")")
            self.kb.kb_retract(r3)


        # Assert start disk on destination peg .. LAST

        next_top = parse_input("fact: (top " + disk1 + " " + peg2 + ")")
        self.kb.kb_assert(next_top)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        tuple_lst = []

        tmp_lst = []
        for i in range(1, 4):
            for j in range(1, 4):
                ask1 = parse_input("fact: (position ?X pos" + str(j) + " pos" + str(i) + ")")
                tile = self.kb.kb_ask(ask1)
                tile = tile[0].bindings_dict["?X"]
                print(tile)
                if tile == "empty":
                    tmp_lst.append(-1)
                else: 
                    tmp_lst.append(int(tile[-1]))
                
            mytuple = tuple(tmp_lst) 
            tmp_lst = []
            tuple_lst.append(mytuple)
        return tuple(tuple_lst)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        
        if not self.isMovableLegal(movable_statement):
            return False 

        tile1 = str(movable_statement.terms[0])
        x1 = str(movable_statement.terms[1])
        y1 = str(movable_statement.terms[2])
        x2 = str(movable_statement.terms[3])
        y2 = str(movable_statement.terms[4])

        # find the tile in the destination (empty)
        ask1 = parse_input("fact: (position ?X " + x2 + " " + y2 + ")")
        ask1 = self.kb.kb_ask(ask1)
        tile2 = ask1[0].bindings_dict["?X"]

        # retract original 
        r1 = parse_input("fact: (position " + tile1 + " " + x1 + " " + y1 + ")")
        self.kb.kb_retract(r1)
        
        # retract destination tile
        r2 = parse_input("fact: (position " + tile2 + " " + x2 + " " + y2 + ")")
        self.kb.kb_retract(r2)

        # assert original tile into new area
        assert1 = parse_input("fact: (position " + tile1 + " " + x2 + " " + y2 + ")")
        self.kb.kb_assert(assert1)

        # assert destination tile into old area
        assert2 = parse_input("fact: (position " + tile2 + " " + x1 + " " + y1 + ")")
        self.kb.kb_assert(assert2)
        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
