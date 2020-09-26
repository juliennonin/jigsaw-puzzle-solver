def find_place_occupied(board):
    list_no_none=[]
    for i in np.arange(len(board)):
        for j in np.arange(len(board[0])):
            if board[i][j] != None:
                list_no_none.append([i,j])

    return list_no_none

def position_to_place(board,n_row,n_column):
    list_no_none = find_place_occupied(board)
    list_number_position_to_place=[]
    for e in list_no_none:

        if board[e[0]][e[1]].right_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e[0]*n_column+e[1]+1])))

        if board[e[0]][e[1]].left_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([e[0]*n_column+e[1]-1])))

        if board[e[0]][e[1]].up_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([(e[0]-1)*n_column+e[1]])))

        if board[e[0]][e[1]].down_occu == False:
            list_number_position_to_place = list(set(list_number_position_to_place).union(set([(e[0]+1)*n_column+e[1]])))


    return list_number_position_to_place