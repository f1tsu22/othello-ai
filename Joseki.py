# �ϐ�����֐�����啝�ɕύX

import json
import information
import OthelloLogic

def joseki(board, moves):

    def getTurns(board): #����ڂł��邩�𒲂ׂ�
        sum0 = 0
        for i in range(8):
            for j in range(8):
                if (board[i][j] == 0):
                    sum0 += 1
        return 64 - sum0 - 3


    def getNewMove(pre_board, board):  #�V���ɑł��ꂽ��̈ʒu���擾
        for i in range(8):
            for j in range(8):
                if (pre_board[i][j] == 0) and (board[i][j] == -1):
                    return [j, i] #������[��,�s]�̌`���ɕϊ�
                    break


    def getReflectPattern(newmove): #�΋ǂ̑��肪�ł��ꂽ�ꏊ���Ƃɏꍇ�����B1�x�������s
        if newmove == [5,4]:   # f5 -> ���̂܂�
            return 1
        elif newmove == [4,5]: # e6 -> ���Ώ�
            return 2
        elif newmove == [2,3]: # c4 -> �_�Ώ�
            return 3
        elif newmove == [3,2]: # d3 -> ���Ώ� + �_�Ώ�
            return 4
        else:
            return 5    #����������U�̏ꍇ


    def reflectIn(newmove, pattern):    #�؍\���̍���[4,5]�ɂȂ�悤�ɕϊ�
                                        # �ϊ���̕ϐ��ɂ͐ړ��� RF ������
        if pattern == 1 or pattern == 5:
            return newmove
        elif pattern == 2:
            return [newmove[1], newmove[0]]
        else:
            i, j = newmove[0] - (newmove[0] - 3.5) * 2, newmove[1] - (newmove[1] - 3.5) * 2
            if pattern == 3:
                return [int(i), int(j)]
            else:
                return [int(j), int(i)]


    def openFile(filename):
        with open(filename, 'r') as f:
            return json.load(f)


    def findBestMove(data, history):
        child = data['children']
        bestmove = None
        for i in range(len(history)-1): 
            for j in range(len(child)):
                tmpchild = child[j] #tmpchild��dict�^
                if history[i+1] == tmpchild['move']:
                    child = tmpchild['children']
                    break
        
        sortByEvaluation = sorted(child, key = lambda x : x['evaluation'], reverse = True)
        options = []
        evaluations = []
        for x in range(len(sortByEvaluation)):
            options.append(sortByEvaluation[x]['move'])
            evaluations.append(sortByEvaluation[x]['evaluation'])
        #print()
        #print('options')
        #print('No,���W,�]���l')
        #for x in range(len(sortByEvaluation)):
            #print(x+1, options[x],evaluations[x])
        #print()

        try:
            bestmove = sortByEvaluation[0]['move']
            BMEvaluation = sortByEvaluation[0]['evaluation']
            print('�I�񂾎� :', bestmove, "  �]���l :", BMEvaluation)
        except:
            bestmove = None
            print('�t�@�C�����Ɏ��̎�̌�₪����܂���ł����B')
        return bestmove
    



    def reflectOut(bestmove, pattern): # �ǂݍ��ݎ��Ƃ͋t�̑Ώ̈ړ�������
        if pattern == 1 or pattern == 5:
            return bestmove
        elif pattern == 2:
            return [bestmove[1], bestmove[0]]
        else:
            i, j = bestmove[0] - (bestmove[0] - 3.5) * 2, bestmove[1] - (bestmove[1] - 3.5) * 2
            if pattern == 3:
                return [int(i), int(j)]
            else:
                return [int(j), int(i)]
    
    # ����������s
    i = information
    turnNum = getTurns(board)
    if i.pre_board != board:
        newMove = getNewMove(i.pre_board, board)
    else:
        newMove = i.pre_bestMove
    if i.step == 0:
        i.pattern = getReflectPattern(newMove)
        print('pattern :', i.pattern)
        i.step = 1
    if turnNum > 1:
        RFnewMove = reflectIn(newMove, i.pattern)
        #print('RFnewMove :', RFnewMove)
        if RFnewMove not in i.history:
            i.history.append(RFnewMove)
    #print('history1 :', i.history)
    data = openFile('Joseki.json')
    try:
        if turnNum > 1:
            RFbestMove = findBestMove(data, i.history)
        else:
            RFbestMove = [5,4]
        #print('�I�񂾎� :', RFbestMove)
        i.history.append(RFbestMove)
        #print('history2 :', i.history)
        bestMove = reflectOut(RFbestMove, i.pattern)
        i.pre_board = OthelloLogic.execute(board, bestMove, 1, 8)
        OthelloLogic.printBoard(i.pre_board)
        i.pre_bestMove = bestMove
        if bestMove not in moves:
            print('�I�񂾎肪���݂̍��@��Ɋ܂܂�Ă��܂���ł����B')
            bestMove = None
    except:
        bestMove = None

    return bestMove