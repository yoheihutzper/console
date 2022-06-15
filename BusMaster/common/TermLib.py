#================================================================
#================================================================
# CONTEC BusMaster Sample for API-DIO(LNX)
# Terminal Operation Library File
#                                                CONTEC Co., Ltd.
#================================================================
#================================================================

import ctypes
import sys
import threading

#================================================================
# マクロ定義
#================================================================
DEC_NUM = 0                 # 10進数
HEX_NUM = 1                 # 16進数
STATUS_AREA_TOP = 0         # 上部ステータスエリア
STATUS_AREA_BOTTOM = 1      # 下部ステータスエリア
MENU_NUM = 10               # メニュー個数
MENU_TIER = 5               # メニュー階層
STATUS_NUM = 5              # ステータス表示最大数
SET_ITEM_MAX_COUNT = 20     # 最大設定項目数
SELECT_ITEM_MAX_COUNT = 30  # 最大選択肢

#================================================================
# エラー定義
#================================================================
TERM_ERR_SUCCESS = 0    # 正常終了
TERM_ERR_INIT    = 1    # 初期化エラー
TERM_ERR_UN_INIT = 2    # 未初期化エラー
TERM_ERR_PARAM   = 3    # パラメータエラー
TERM_ERR_INIT_SCR= 4    # ウィンドウ生成失敗
TERM_ERR_DUP_EXEC= 5    # 重複実行エラー

term_data = {
    'main_window_menu_tier':0,      # メインウインドウデータ
    'set_window_menu_tier':0,       # 設定ウインドウデータ
    'active_window_menu_tier':0,    # アクティブなウインドウデータ
    'caption_str':'',               # 現在のキャプション
    'pre_caption_str':'',           # 直前のキャプション
    'status_top_name':'',           # 上部ステータスエリア名
    'status_buttom_name':'',        # 下部ステータスエリア名
    'menu':[],                      # メニュー[メニュー個数] 現在使用しているメニュー
    'pre_menu':[]                   # メニュー[メニュー個数] 直前のメニュー
}

lock = threading.Lock()

#================================================================
# 文字列を数値に変換できるかどうか確認する関数
#================================================================
def isnum(str, base):
    try:
        if 16 == base:
            int(str, 16)
        else:
            int(str)
    except:
        return False
    return True

#================================================================
# 設定画面情報表示関数
#================================================================
def TermSetInfoWindow(set_scr):
    #----------------------------------------
    # パラメータチェック
    #----------------------------------------
    if len(set_scr) == 0:
        return TERM_ERR_PARAM
    #----------------------------------------
    # 仕切りの表示
    #----------------------------------------
    print('\n------------------------------')
    #----------------------------------------
    # 項目選択タイプ設定情報表示
    #----------------------------------------
    for select_item in set_scr['select_item']:
        if select_item['set_item_name'] != '':
            print('{0:<20s}: {1:s}'.format(select_item['set_item_name'], select_item['item'][select_item['set_num']]['name']))
    #----------------------------------------
    # 数値入力タイプ設定情報表示
    #----------------------------------------
    for item in set_scr['input_num']:
        #----------------------------------------
        # 10進数表示タイプならば
        #----------------------------------------
        if item['hex_or_dec'] == DEC_NUM:
            if item['unit_name'] != '':
                print('{0:<20s}: {1:d} [{2:s}]'.format(item['set_item_name'], item['set_num'], item['unit_name']))
            else:
                print('{0:<20s}: {1:d}'.format(item['set_item_name'], item['set_num']))
        #----------------------------------------
        # 16進数表示タイプならば
        #----------------------------------------
        else:
            if item['unit_name'] != '':
                print('{0:<20s}: {1:X} [{2:s}]'.format(item['set_item_name'], item['set_num'], item['unit_name']))
            else:
                print('{0:<20s}: {1:X}'.format(item['set_item_name'], item['set_num']))
    #----------------------------------------
    # 仕切りの表示
    #----------------------------------------
    print('------------------------------\n')

    return TERM_ERR_SUCCESS

#================================================================
# 初期化関数
#================================================================
def TermInit(main_scr):
    count = 0

    #----------------------------------------
    # パラメータチェック
    #----------------------------------------
    if len(main_scr) == 0:    # main_srcがNULLの場合
        return TERM_ERR_PARAM
    #----------------------------------------
    # グローバルデータ初期化
    #----------------------------------------
    term_data['main_window_menu_tier'] = 0
    term_data['set_window_menu_tier'] = 0
    term_data['active_window_menu_tier'] = 0
    term_data['caption_str'] = ''
    term_data['pre_caption_str'] = ''
    term_data['status_top_name'] = ''
    term_data['status_buttom_name'] = ''
    term_data['menu'].clear()
    term_data['pre_menu'].clear()
    #----------------------------------------
    # メニュー階層数取得
    #----------------------------------------
    while count < MENU_NUM:
        if main_scr['menu'][count] == []:
            break
        count += 1
    #----------------------------------------
    # ステータスエリア名設定
    #----------------------------------------
    term_data['status_top_name'] = main_scr['status_top_name']
    term_data['status_buttom_name'] = main_scr['status_buttom_name']
    #----------------------------------------
    # 初期表示データ設定
    #----------------------------------------
    #----------------------------------------
    # ウインドウ名設定
    #----------------------------------------
    term_data['caption_str'] = main_scr['app_name']
    #----------------------------------------
    # メニュー表示設定
    #----------------------------------------
    TermMenuSet(main_scr['menu'][0].copy())

    return TERM_ERR_SUCCESS


#================================================================
# 終了関数
#================================================================
def TermExit():
    #----------------------------------------
    # グローバルデータ初期化
    #----------------------------------------
    term_data['main_window_menu_tier'] = 0
    term_data['set_window_menu_tier'] = 0
    term_data['active_window_menu_tier'] = 0
    term_data['caption_str'] = ''
    term_data['pre_caption_str'] = ''
    term_data['status_top_name'] = ''
    term_data['status_buttom_name'] = ''
    term_data['menu'].clear()
    term_data['pre_menu'].clear()

    return TERM_ERR_SUCCESS


#================================================================
# メニュー設定関数
#================================================================
def TermMenuSet(menu):
    global lock

    #----------------------------------------
    # 排他制御開始
    #----------------------------------------
    lock.acquire()
    #----------------------------------------
    # メニューデータコピー
    #----------------------------------------
    term_data['menu'].clear()
    for item in menu:
        term_data['menu'].append(item)
    #----------------------------------------
    # 仕切りの表示
    #----------------------------------------
    print('\n==============================')
    print(term_data['caption_str'])
    print('==============================')
    #----------------------------------------
    # メニュー表示設定
    #----------------------------------------
    count = 0
    for item in menu:
        print('{}.{}'.format(count, item))
        count += 1
    #----------------------------------------
    # 仕切りの表示
    #----------------------------------------
    print('==============================\n')
    #----------------------------------------
    # 排他制御終了
    #----------------------------------------
    lock.release()

    return TERM_ERR_SUCCESS


#================================================================
# メニュー番号取得関数
#================================================================
def TermGetMenuNum(message, menu_num):
    #----------------------------------------
    # パラメータチェック
    #----------------------------------------
    if message == '':
        return TERM_ERR_PARAM, 0
    #----------------------------------------
    # メッセージ表示
    #----------------------------------------
    print('{}: '.format(message))
    #----------------------------------------
    # 数値入力(0-9)
    #----------------------------------------
    valid_nums = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9}
    menu_num = -1
    while menu_num == -1:
        str = input()
        if str in valid_nums.keys():
            menu_num = valid_nums[str]
    #----------------------------------------
    # メニュー表示
    #----------------------------------------
    TermMenuSet(term_data['menu'].copy())
    
    return TERM_ERR_SUCCESS, menu_num


#================================================================
# 文字列取得関数
#================================================================
def TermGetStr(message, get_str):
    #----------------------------------------
    # パラメータチェック
    #----------------------------------------
    if len(message) == 0:
        return (TERM_ERR_PARAM, '')
    #----------------------------------------
    # メッセージ表示
    #----------------------------------------
    print('{}\n: '.format(message), end='')
    #----------------------------------------
    # 文字列入力
    #----------------------------------------
    get_str = input()
    #----------------------------------------
    # メニュー表示
    #----------------------------------------
    TermMenuSet(term_data['menu'].copy())

    return TERM_ERR_SUCCESS, get_str


#================================================================
# ステータス文字列設定関数
#================================================================
def TermSetStatus(sts_area, item_name, status_str, new_line=True):
    global lock

    #----------------------------------------
    # 排他制御開始
    #----------------------------------------
    lock.acquire()
    #----------------------------------------
    # パラメータチェック
    #----------------------------------------
    if item_name == '':
        return TERM_ERR_PARAM
    #----------------------------------------
    # ステータス文字列設定
    #----------------------------------------
    if new_line == False:
        if sts_area == STATUS_AREA_TOP:
            print('\r{} {:<10s}: {}'.format(term_data['status_top_name'], item_name, status_str), end='', flush=True)
        else:
            print('\r{} {:<10s}: {} '.format(term_data['status_buttom_name'], item_name, status_str), end='', flush=True)
    else:
        if sts_area == STATUS_AREA_TOP:
            print('{} {:<10s}: {}'.format(term_data['status_top_name'], item_name, status_str))
        else:
            print('{} {:<10s}: {}'.format(term_data['status_buttom_name'], item_name, status_str))
    #----------------------------------------
    # 排他制御終了
    #----------------------------------------
    lock.release()

    return TERM_ERR_SUCCESS


#================================================================
# 設定画面初期化関数
#================================================================
def TermSetWindowOpen(set_scr):
    count = 0

    #----------------------------------------
    # パラメータチェック
    #----------------------------------------
    if len(set_scr) == 0:
        return TERM_ERR_PARAM
    #----------------------------------------
    # メニュー階層数取得
    #----------------------------------------
    while count < MENU_NUM:
        if set_scr['menu'][count] == []:
            break
        count += 1
    term_data['set_window_menu_tier'] = count
    #----------------------------------------
    # 表示データ設定
    #----------------------------------------
    term_data['pre_caption_str'] = term_data['caption_str']
    term_data['caption_str'] = set_scr['window_name']
    #----------------------------------------
    # メニューデータコピー
    #----------------------------------------
    term_data['pre_menu'].clear()
    for item in term_data['menu']:
        term_data['pre_menu'].append(item)
    TermMenuSet(set_scr['menu'][0].copy())
    #----------------------------------------
    # 設定画面情報表示
    #----------------------------------------
    TermSetInfoWindow(set_scr)

    return TERM_ERR_SUCCESS


#================================================================
# 設定画面終了関数
#================================================================
def TermSetWindowClose():
    #----------------------------------------
    # ウインドウ名設定
    #----------------------------------------
    term_data['caption_str'] = term_data['pre_caption_str']
    #----------------------------------------
    # メインメニューに戻る
    #----------------------------------------
    TermMenuSet(term_data['pre_menu'].copy())

    return TERM_ERR_SUCCESS


#================================================================
# 設定内容取得関数(項目選択)
#================================================================
def TermGetSelectItem(set_scr, item_num, select_num):
    #----------------------------------------
    # パラメータチェック
    #----------------------------------------
    if len(set_scr) == 0:
        return TERM_ERR_PARAM
    #----------------------------------------
    # 項目名表示
    #----------------------------------------
    print('< {} >'.format(set_scr['select_item'][item_num]['set_item_name']))
    #----------------------------------------
    # 質問表示
    #----------------------------------------
    print('Please choose from the following choice.')
    #----------------------------------------
    # 選択項目表示
    #----------------------------------------
    buf = '\n'
    count = 0
    for item in set_scr['select_item'][item_num]['item']:
        buf = str.format('{0:s}{1:d}. {2:s}  ', buf, count + 1, item['name'])
        count += 1
    #----------------------------------------
    # 最大項目数保存
    #----------------------------------------
    max_count = count
    while True:
        #----------------------------------------
        # 回答入力
        #----------------------------------------
        print('{}\n> '.format(buf), end='')
        str_input = input()
        if False == isnum(str_input, 10):
            continue
        input_num = int(str_input)
        if 0 < input_num and input_num <=  max_count:
            break
    #----------------------------------------
    # 入力値を設定画面データに設定
    #----------------------------------------
    set_scr['select_item'][item_num]['set_num'] = input_num - 1
    #----------------------------------------
    # 返却データを設定
    #----------------------------------------
    select_num = set_scr['select_item'][item_num]['item'][input_num - 1]['num']
    #----------------------------------------
    # 設定情報表示
    #----------------------------------------
    TermSetInfoWindow(set_scr)
    #----------------------------------------
    # メニュー表示
    #----------------------------------------
    TermMenuSet(term_data['menu'].copy())

    return TERM_ERR_SUCCESS, select_num


#================================================================
# 設定内容取得関数(数値入力)
#================================================================
def TermGetInputNum(set_scr, item_num, input_num):
    #----------------------------------------
    # パラメータチェック
    #----------------------------------------
    if len(set_scr) == 0:
        return (TERM_ERR_PARAM, 0)
    #----------------------------------------
    # 項目名表示
    #----------------------------------------
    print('< {} >'.format(set_scr['input_num'][item_num]['set_item_name']))
    #----------------------------------------
    # 質問表示
    #----------------------------------------
    while True:
        print('Please input a setting value.')
        #----------------------------------------
        # プロンプト表示
        #----------------------------------------
        if set_scr['input_num'][item_num]['unit_name'] != '':
            print('[{}]:'.format(set_scr['input_num'][item_num]['unit_name']), end='')
        else:
            print(':', end='')
        #----------------------------------------
        # 回答入力
        #----------------------------------------
        #----------------------------------------
        # 10進数ならば
        #----------------------------------------
        if set_scr['input_num'][item_num]['hex_or_dec'] == DEC_NUM:
            str = input()
            if False == isnum(str, 10):
                continue
            input_num = int(str)
            break
        #----------------------------------------
        # 16進数ならば
        #----------------------------------------
        else:
            str = input()
            if False == isnum(str, 16):
                continue
            input_num = int(str, base=16)
            break
    #----------------------------------------
    # 入力値を設定画面データに設定
    #----------------------------------------
    set_scr['input_num'][item_num]['set_num'] = input_num
    #----------------------------------------
    # 設定情報表示
    #----------------------------------------
    TermSetInfoWindow(set_scr)
    #----------------------------------------
    # メニュー表示
    #----------------------------------------
    TermMenuSet(term_data['menu'].copy())
    
    return TERM_ERR_SUCCESS, input_num