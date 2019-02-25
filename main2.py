import unittest, inspect
from multiprocessing.pool import ThreadPool
from multiprocessing.context import TimeoutError
from student_code_game_masters import *
from student_code_uninformed_solvers import *

class KBTest(unittest.TestCase):

    def setUp(self):
        self.pool = ThreadPool(processes=1)
        self.lastEndStep = 0

    def playXSteps(self, solver, plays):
        """
        Call the solver's solveOneStep for x times, and record the result game state

        Args:
             solver: solver of the game
             plays: list of lists; inner list consists of the number of steps (x) followed by the expected outcome
        """
        res = []
        for play in plays:
            x = play[0]
            while self.lastEndStep < x:
                solver.solveOneStep()
                self.lastEndStep += 1
            res.append(solver.gm.getGameState())
        return res

    def solve(self, solver):
        """
        Call the solver's solve function, which should solve the game.

        Args:
             solver: solver of the game
        """
        solver.solve()

    def runPlayXSteps(self, solver, plays, timeout=5):
        """
        Wrapper function; calls playXSteps(..) with a timeout

        Args:
             solver: solver of the game
             plays: list of lists; inner list consists of the number of steps (x) followed by the expected outcome
             timeout: time out in seconds. Default 5 seconds
        """
        try:
            results = self.pool.apply_async(self.playXSteps, [solver, plays]).get(timeout)
            for index, play in enumerate(plays):
                expected = play[1]
                self.assertEqual(results[index], expected)
        except TimeoutError:
            raise Exception("Timed out: %s" % inspect.stack()[1][3])

    def runSolve(self, solver, timeout=5):
        """
        Wrapper function; calls solve(..) with a timeout

        Args:
             solver: solver of the game
             timeout: time out in seconds. Default 5 seconds
        """
        try:
            self.pool.apply_async(self.solve, [solver,]).get(timeout)
            self.assertTrue(solver.gm.isWon())
        except TimeoutError:
            raise Exception("Timed out: %s" % inspect.stack()[1][3])

    def test0555_Hanoi(self):
        th = TowerOfHanoiGame()
        th.read('hanoi_5_two_smallest_on_peg_three.txt')
        required = [
            'fact: (movable disk1 peg3 peg1)',
            'fact: (movable disk1 peg3 peg2)',
        ]
        th.setWinningCondition(required, 'hanoi_all_forbidden.txt')
        self.assertFalse(th.isWon())
        solver = SolverBFS(th, ((),(),(1,2,3)))
        self.runSolve(solver,)

    
if __name__ == '__main__':
    unittest.main()