# 変数名や関数名を大幅に変更

import json
import information
import OthelloLogic

def joseki(board, moves):

    def getTurns(board): #何手目であるかを調べる
        sum0 = 0
        for i in range(8):
            for j in range(8):
                if (board[i][j] == 0):
                    sum0 += 1
        return 64 - sum0 - 3


    def getNewMove(pre_board, board):  #新たに打たれた手の位置を取得
        for i in range(8):
            for j in range(8):
                if (pre_board[i][j] == 0) and (board[i][j] == -1):
                    return [j, i] #ここで[列,行]の形式に変換
                    break


    def getReflectPattern(newmove): #対局の第一手が打たれた場所ごとに場合分け。1度だけ実行
        if newmove == [5,4]:   # f5 -> そのまま
            return 1
        elif newmove == [4,5]: # e6 -> 線対称
            return 2
        elif newmove == [2,3]: # c4 -> 点対称
            return 3
        elif newmove == [3,2]: # d3 -> 線対称 + 点対称
            return 4
        else:
            return 5    #こっちが先攻の場合


    def reflectIn(newmove, pattern):    #木構造の根が[4,5]になるように変換
                                        # 変換後の変数には接頭語 RF をつける
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
                tmpchild = child[j] #tmpchildはdict型
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
        #print('No,座標,評価値')
        #for x in range(len(sortByEvaluation)):
            #print(x+1, options[x],evaluations[x])
        #print()

        try:
            bestmove = sortByEvaluation[0]['move']
            BMEvaluation = sortByEvaluation[0]['evaluation']
            print('選んだ手 :', bestmove, "  評価値 :", BMEvaluation)
        except:
            bestmove = None
            print('ファイル内に次の手の候補がありませんでした。')
        return bestmove
    



    def reflectOut(bestmove, pattern): # 読み込み時とは逆の対称移動をする
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
    
    # ここから実行
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
        #print('選んだ手 :', RFbestMove)
        i.history.append(RFbestMove)
        #print('history2 :', i.history)
        bestMove = reflectOut(RFbestMove, i.pattern)
        i.pre_board = OthelloLogic.execute(board, bestMove, 1, 8)
        OthelloLogic.printBoard(i.pre_board)
        i.pre_bestMove = bestMove
        if bestMove not in moves:
            print('選んだ手が現在の合法手に含まれていませんでした。')
            bestMove = None
    except:
        bestMove = None

    return bestMove