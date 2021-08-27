"""
Quartoゲーム実行コマンド
python python/run.py [arg1] [arg2] [arg3]
arg1:対戦回数 数字で入力
arg2:マルチプロセスの実行 'm'を入力でマルチプロセス 未入力 or 'm'以外でシングルプロセス
arg3:ログのファイル出力 '1'を入力でログファイル生成 未入力 or '1'以外でログファイルを生成しない
"""

from ..utils import gamemain, util
from ..AI.montecarlo_ai import Montecarlo

import click
import sys
import time
import math
from datetime import datetime

@click.command()
@click.argument('your_ai')
@click.argument('opponent_ai')
@click.option('--matches', type = int, default = 1, help = 'Number of matches (default: 1)')

def multiprocRun(your_ai, opponent_ai, matches):
    st = time.time()
    matches = math.ceil(matches/2)#勝敗の均等性をとるため、1回の処理で先行後攻の2回は必ずまわす。よって、2で割って切り上げた回数を指定。

    your_ai_klass = globals()[your_ai]
    your_ai_instance = your_ai_klass()

    opponent_ai_klass = globals()[opponent_ai]
    opponent_ai_instance = opponent_ai_klass()

    result = gamemain.winningPercentageRunMultiprocess([matches, your_ai_instance, opponent_ai_instance])

    #ログ出力
    total = 0
    win1 = 0
    win2 = 0
    draw = 0
    total += result['対戦回数：']
    win1 += result['AI1勝利数：']
    win2 += result['AI2勝利数：']
    draw += result['引き分け数：']
    util.p.print(str(result))

    util.p.print('')
    util.p.print('len result:'+str(len(result)))
    util.p.print('全体対戦回数：'+str(total))
    util.p.print('全体AI1勝率：'+str(win1/total*100))
    util.p.print('全体AI2勝率：'+str(win2/total*100))
    util.p.print('全体引き分け率：'+str(draw/total*100))
    util.p.print('全体処理時間：'+str(time.time()-st))


if __name__ == "__main__":
    #１つ目のパラメータに数字を入力されたらその回数だけ対戦をする
    num = 1
    if len(sys.argv) >= 2:
        num = int(sys.argv[1])

    #２つ目のパラメータに'm'と入力されたらマルチプロセスで実行
    multiflag = False
    if len(sys.argv) >= 3 and sys.argv[2] == 'm':
        multiflag = True
    
    #３つ目のパラメータに'1'と入力されたらログファイルを出力
    outputlog = False
    if len(sys.argv) >= 4 and sys.argv[3] == '1':
        outputlog = True
    
    #ログファイルを開く
    if(outputlog):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        util.p.open('quarto_'+timestamp+'.log')

    #ゲームを実行
    if multiflag:   multiprocRun(num)
    else:           singleprocRun(num)
        
    #ログファイルを閉じる
    util.p.close()
