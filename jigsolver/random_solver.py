import numpy as np
from jigsolver.puzzle import Piece

def random_solver(puzzle,plotsteps=True):
    '''Solve a puzzle randomly'''

    # Random solver
    np.random.shuffle(puzzle.bag_of_pieces)

    # Simulate solver step by step
    for i in range(puzzle.shape[0]):
        for j in range(puzzle.shape[1]):
            if puzzle.board[i][j] == None: ## If location empty
                puzzle.board[i][j] = puzzle.bag_of_pieces[0]
                puzzle.bag_of_pieces = puzzle.bag_of_pieces[1:]

                if plotsteps == True : # Plot puzzle at step
                    puzzle.plot()

    return

def place_pieces(puzzle,matrix):
    pieces_total = len(puzzle.bag_of_pieces)
    puzzle.board_space[len(puzzle.board_space[0]) // 2][len(puzzle.board_space) // 2] = puzzle.get_piece(0)
    puzzle.set_piece_in_space(0)
    while(1):
        compare_list = [e for e in filter(lambda x: x.in_space == False, puzzle.bag_of_pieces)]
        in_space_list = [e for e in filter(lambda x: x.in_space == True, puzzle.bag_of_pieces)]
        if compare_list[0] != []:
            right_side_list = [e for e in filter(lambda x: x.right_occu == False, in_space_list)]
            left_side_list = [e for e in filter(lambda x: x.left_occu == False, in_space_list)]
            up_side_list = [e for e in filter(lambda x: x.up_occu == False, in_space_list)]
            down_side_list = [e for e in filter(lambda x: x.down_occu == False, in_space_list)]
            return
            position,number_piece_to_place,side,number_piece_near = get_best([right_side_list,left_side_list,up_side_list,down_side_list],matrix)
            place_piece_to_position(position, number_piece_to_place, side, number_piece_near)

            # return


        else: return print("finish")


    def get_best_piece(list,matrix):

        ...

        return position,number_piece_to_place,side,number_piece_near



