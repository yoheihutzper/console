#================================================================
#================================================================
# API-DIO(LNX)
# 入出力サンプル
#                                                CONTEC Co., Ltd.
#================================================================
#================================================================

import ctypes
import sys
import cdio

#================================================================
# コマンド定義
#================================================================
COMMAND_ERROR = 0      # エラー
COMMAND_INP_PORT = 1   # 1ポート入力
COMMAND_INP_BIT = 2    # 1ビット入力
COMMAND_OUT_PORT = 3   # 1ポート出力
COMMAND_OUT_BIT = 4    # 1ビット出力
COMMAND_ECHO_PORT = 5  # 1ポートエコーバック
COMMAND_ECHO_BIT = 6   # 1ビットエコーバック
COMMAND_QUIT = 7       # 終了


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
# main関数
#================================================================
def main():
    dio_id = ctypes.c_short()
    io_data = ctypes.c_ubyte()
    port_no = ctypes.c_short()
    bit_no = ctypes.c_short()
    err_str = ctypes.create_string_buffer(256)

    #----------------------------------------
    # ドライバ初期化処理
    #----------------------------------------
    dev_name = input('Input device name: ')
    lret = cdio.DioInit(dev_name.encode(), ctypes.byref(dio_id))
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioInit = {lret}: {err_str.value.decode('sjis')}")
        sys.exit()
    #----------------------------------------
    # 入力待ちループ
    #----------------------------------------
    while True:
        #----------------------------------------
        # コマンドの表示
        #----------------------------------------
        print('')
        print('--------------------')
        print(' Menu')
        print('--------------------')
        print('ip : port input')
        print('ib : bit  input')
        print('op : port output')
        print('ob : bit  output')
        print('ep : port echoback')
        print('eb : bit  echoback')
        print('q  : quit')
        print('--------------------')
        buf = input('input command: ')
        #----------------------------------------
        # コマンドの識別
        #----------------------------------------
        command = COMMAND_ERROR
        #----------------------------------------
        # 1ポート入力
        #----------------------------------------
        if buf == 'ip':
            command = COMMAND_INP_PORT
        #----------------------------------------
        # 1ビット入力
        #----------------------------------------
        if buf == 'ib':
            command = COMMAND_INP_BIT
        #----------------------------------------
        # 1ポート出力
        #----------------------------------------
        if buf == 'op':
            command = COMMAND_OUT_PORT
        #----------------------------------------
        # 1ビット出力
        #----------------------------------------
        if buf == 'ob':
            command = COMMAND_OUT_BIT
        #----------------------------------------
        # 1ポートエコーバック
        #----------------------------------------
        if buf == 'ep':
            command = COMMAND_ECHO_PORT
        #----------------------------------------
        # 1ビットエコーバック
        #----------------------------------------
        if buf == 'eb':
            command = COMMAND_ECHO_BIT
        #----------------------------------------
        # 終了
        #----------------------------------------
        if buf == 'q':
            command = COMMAND_QUIT
        #----------------------------------------
        # ポート番号、ビット番号の入力
        #----------------------------------------
        if(command == COMMAND_INP_PORT or
           command == COMMAND_OUT_PORT or
           command == COMMAND_ECHO_PORT):
           while True:
                buf = input('input port number: ')
                if False == isnum(buf, 10):
                   continue
                port_no = ctypes.c_short(int(buf))
                break
        elif(command == COMMAND_INP_BIT or
             command == COMMAND_OUT_BIT or
             command == COMMAND_ECHO_BIT):
             while True:
                buf = input('input bit number: ')
                if False == isnum(buf, 10):
                   continue
                bit_no = ctypes.c_short(int(buf))
                break
        #----------------------------------------
        # データの入力
        #----------------------------------------
        if(command == COMMAND_OUT_PORT or
           command == COMMAND_OUT_BIT):
           while True:
                buf = input('input data (hex): ')
                if False == isnum(buf, 16):
                   continue
                io_data = ctypes.c_ubyte(int(buf, 16))
                break
        #----------------------------------------
        # コマンドの実行と結果の表示
        #----------------------------------------
        #----------------------------------------
        # 1ポート入力
        #----------------------------------------
        if command == COMMAND_INP_PORT:
            lret = cdio.DioInpByte(dio_id, port_no, ctypes.byref(io_data))
            if lret == cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, err_str)
                print(f'DioInpByte port = {port_no.value}: data = 0x{io_data.value:02x}')
            else:
                cdio.DioGetErrorString(lret, err_str)
                print(f"DioInpByte = {lret}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # 1ビット入力
        #----------------------------------------
        elif command == COMMAND_INP_BIT:
            lret = cdio.DioInpBit(dio_id, bit_no, ctypes.byref(io_data))
            if lret == cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, err_str)
                print(f'DioInpBit port = {bit_no.value}: data = 0x{io_data.value:02x}')
            else:
                cdio.DioGetErrorString(lret, err_str)
                print(f"DioInpBit = {lret}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # 1ポート出力
        #----------------------------------------
        elif command == COMMAND_OUT_PORT:
            lret = cdio.DioOutByte(dio_id, port_no, io_data)
            if lret == cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, err_str)
                print(f'DioOutByte port = {port_no.value}: data = 0x{io_data.value:02x}')
            else:
                cdio.DioGetErrorString(lret, err_str)
                print(f"DioOutByte = {lret}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # 1ビット出力
        #----------------------------------------
        elif command == COMMAND_OUT_BIT:
            lret = cdio.DioOutBit(dio_id, bit_no, io_data)
            if lret == cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, err_str)
                print(f'DioOutBit port = {bit_no.value}: data = 0x{io_data.value:02x}')
            else:
                cdio.DioGetErrorString(lret, err_str)
                print(f"DioOutBit = {lret}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # 1ポートエコーバック
        #----------------------------------------
        elif command == COMMAND_ECHO_PORT:
            lret = cdio.DioEchoBackByte(dio_id, port_no, ctypes.byref(io_data))
            if lret == cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, err_str)
                print(f'DioEchoBackByte port = {port_no.value}: data = 0x{io_data.value:02x}')
            else:
                cdio.DioGetErrorString(lret, err_str)
                print(f"DioEchoBackByte = {lret}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # 1ビットエコーバック
        #----------------------------------------
        elif command == COMMAND_ECHO_BIT:
            lret = cdio.DioEchoBackBit(dio_id, bit_no, ctypes.byref(io_data))
            if lret == cdio.DIO_ERR_SUCCESS:
                cdio.DioGetErrorString(lret, err_str)
                print(f'DioEchoBackBit port = {bit_no.value}: data = 0x{io_data.value:02x}')
            else:
                cdio.DioGetErrorString(lret, err_str)
                print(f"DioEchoBackBit = {lret}: {err_str.value.decode('sjis')}")
        #----------------------------------------
        # 終了
        #----------------------------------------
        elif command == COMMAND_QUIT:
            print(f'quit.')
            break
        #----------------------------------------
        # エラー
        #----------------------------------------
        elif command == COMMAND_ERROR:
            print(f'error: {buf}.')
            break
    #----------------------------------------
    # ドライバ終了処理
    #----------------------------------------
    lret = cdio.DioExit(dio_id)
    if lret != cdio.DIO_ERR_SUCCESS:
        cdio.DioGetErrorString(lret, err_str)
        print(f"DioExit = {lret}: {err_str.value.decode('sjis')}")
    #----------------------------------------
    # アプリケーション終了
    #----------------------------------------
    sys.exit()


#----------------------------------------
# main関数呼び出し
#----------------------------------------
if __name__ == "__main__":
    main()
