from copy import deepcopy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the length of the sentence equals the count,
        # all cells are mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
    

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the sentence (of length > 0) has a count of 0,
        # all cells are safe.
        if len(self.cells):
            if self.count == 0:
                print(f'Is it a set: {self.cells}')
                return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Check whether the cell is in the sentence,
        # then remove, and reduce count by 1 (one less mine)
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Check whether the cell is in the sentence,
        # then remove, and don't change count (no more or less mines)
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
        print(f'Current list of mines: {self.mines}')

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Add the made move (cell) to the corresponding set
        self.moves_made.add(cell)

        # Mark cell as safe, and update all sentences with
        # this information
        self.mark_safe(cell)

        # Add new sentence to the AI knowledge base
        # Loop over all the neighbouring cells to see
        # whether they can be added to the sentence
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                temp_cell = (i, j)

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is not
                # an already made move nor a known safe.
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (temp_cell not in self.moves_made) and (temp_cell not in self.safes):
                        cells.add(temp_cell)
        
        new_sentence = Sentence(cells, count)
        
        # Only add the sentence if it's not empty
        if new_sentence.cells != set():
            self.knowledge.append(new_sentence)
            print(f'The added sentence is: {new_sentence}')

        # See if any sentences in the knowledge base
        # hold information about safes/mines.
        # Copy first, because otherwise you get errors
        # for changing the set over which you are looping
        self.knowledge_copy = deepcopy(self.knowledge)
        
        for sentence in self.knowledge_copy:
            #print(f'loop which marks sentences their safes and mines, current sentence: {sentence}')
            if len(sentence.cells):
                if len(sentence.cells) == sentence.count:
                    for cell in sentence.cells:
                        self.mark_mine(cell)
                elif sentence.count == 0:
                    for cell in sentence.cells:
                        self.mark_safe(cell)

        # Check whether a sentence is a subset of another.
        # If so, substract subset from superset
        # and as such, generate new knowledge.
        if len(self.knowledge) > 1:
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence2.cells != set() and sentence1.cells != set():
                        if sentence2.cells.issubset(sentence1.cells) and sentence1 != sentence2:
                            sentence3 = Sentence(sentence1.cells - sentence2.cells, sentence1.count - sentence2.count)
                            print(f'Sentence 2: {sentence2} is a subset of Sentence 1: {sentence1} forming inference: {sentence3}')
                            if (sentence3.cells != set()) and (sentence3 not in self.knowledge):
                                self.knowledge.append(sentence3)
                                print(f'{sentence2} is a subset of {sentence1}, yielding new knowledge {sentence3}')
        
        self.knowledge_copy = deepcopy(self.knowledge)
        for sentence in self.knowledge_copy:
            #print(f'loop which marks sentences their safes and mines, current sentence: {sentence}')
            if len(sentence.cells):
                if len(sentence.cells) == sentence.count:
                    for cell in sentence.cells:
                        self.mark_mine(cell)
                elif sentence.count == 0:
                    for cell in sentence.cells:
                        self.mark_safe(cell)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_move in self.safes:
            if safe_move not in self.moves_made and safe_move not in self.mines:
                print(safe_move)
                return safe_move

        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Currently the loop generates up to 64 random cells
        # However, this is not perfect, as sometimes same cell
        # get chosen twice inside 64 attempts. Not only problem
        # with the way the function now is I think. But still,
        # should work most of the time and won't return a
        # made move nor a mine.
        count = 0
        
        while count < (self.height * self.width):
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            cell = (i, j)
            if cell not in self.moves_made:
                if cell not in self.mines:
                    return cell
                else:
                    count += 1
        return None