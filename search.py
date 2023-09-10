import time
from collections import deque
import psutil
import sys

class Search:

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def get_moves(self, board):
        moves = []
        empty_row, empty_col = None, None

        for i in range(4):
            for j in range(4):
                if board[i][j] == '0':
                    empty_row, empty_col = i, j  # find the position of the empty space
                    break

        # Right move
        if (empty_col + 1 < 4):
            new_board = [list(row) for row in board]

            new_board[empty_row][empty_col], new_board[empty_row][empty_col + 1] = \
                new_board[empty_row][empty_col + 1], new_board[empty_row][empty_col]

            moves.append((new_board, 'R'))

        # Left move
        if (empty_col - 1 >= 0):
            new_board = [list(row) for row in board]

            new_board[empty_row][empty_col], new_board[empty_row][empty_col - 1] = \
                new_board[empty_row][empty_col - 1], new_board[empty_row][empty_col]

            moves.append((new_board, 'L'))

        # Down move
        if (empty_row + 1 < 4):
            new_board = [list(row) for row in board]

            new_board[empty_row][empty_col], new_board[empty_row + 1][empty_col] = \
                new_board[empty_row + 1][empty_col], new_board[empty_row][empty_col]

            moves.append((new_board, 'D'))

        # Up move
        if (empty_row - 1 >= 0):
            new_board = [list(row) for row in board]

            new_board[empty_row][empty_col], new_board[empty_row - 1][empty_col] = \
                new_board[empty_row - 1][empty_col], new_board[empty_row][empty_col]

            moves.append((new_board, 'U'))

        return moves

    def bfs(self, initial_board):
        visited = set()
        queue = deque([(initial_board, "")])
        # queue containing the elements (board,moves to get this board)
        expanded_nodes = 0

        while queue:
            current_board, moves = queue.popleft()  # pop the current board
            expanded_nodes += 1 #increase the number of expanded nodes

            # take the current board and convert it into a vector in order to check the solution
            current_board_vector = [tile for row in current_board for tile in row]

            if self.goal_test(current_board_vector): #solution check
                return moves, expanded_nodes, time.time(), psutil.Process().memory_info().rss / 1024

            #add at the visited set the current board, in this way, if we encounter it in a future iteration
            # we will ignore it, in this way we optimize the bfs
            visited.add(tuple(map(tuple, current_board)))


            #iterating over the possible moves (at most 4), if we find an already visited configuration, we ignore it,
            #otherwise, we add it to the queue of configurations
            for next_board, move in self.get_moves(current_board):
                if tuple(map(tuple, next_board)) not in visited:
                    queue.append((next_board, moves + move))
        return

    def solve(self, input):  # Format : "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"

        initial_list = input.split(" ")
        initial_board = [[initial_list[i + j] for j in range(4)] for i in range(0, len(initial_list), 4)]

        initial_memory= psutil.Process().memory_info().rss / 1024
        start_time = time.time()
        result = self.bfs(initial_board)
        moves, expanded_nodes, end_time, total_memory = result

        print("Moves:", moves)
        print("Number of expanded Nodes:", expanded_nodes)
        print("Time Taken:", round(end_time - start_time, 3), "seconds")
        print("Max Memory (KB):", round(total_memory-initial_memory, 2))

        return "".join(moves)  # Get the list of moves to solve the puzzle. Format is "RDLDDRR"


if __name__ == '__main__':
    # Access command-line arguments
    arguments = sys.argv[1:]  # Exclude the first argument, which is the script name

    #convert the arguments in a string (input of the bfs)
    input_str = " ".join(arguments)
    
    #perform the search
    agent = Search()
    agent.solve(input_str)
