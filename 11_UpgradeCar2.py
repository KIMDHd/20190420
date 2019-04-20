import msvcrt
import serial
import time

# ------------------------------------------------------------------------------------------------------
# Function: to send command (string with new line) to micro:bit
# 함수: micro:bit에 명령 보내기 (새로운 줄의 문자열)
# Input: Cmd - the string command to send (one character)
# 입력: Cmd - 문자열 명령어를 보냄(하나의 문자도 가능)
# Return: none
# 돌아가기: 없음
# ------------------------------------------------------------------------------------------------------
def SerialSendCommand(ser, Cmd):
    Cmd_Str = Cmd + '\n'
    cmd_bytes = str.encode(Cmd_Str)
    ser.write(cmd_bytes)

# ------------------------------------------------------------------------------------------------------
# Function: to receive response from micro:bit
# 함수: 마이크로비트에서 대답 받기
# Input: Cmd - the string expecting to receive (one character)
# 입력: Cmd - 문자열 예상를 수신 (하나의 문자)
# Return: ret = 1 correct response received, -1 = incorrect/no response received
# 반환: ret = 1개의 올바른 응답을 수신함, -1 = 부정확함/응답 없음
# ------------------------------------------------------------------------------------------------------
def SerialReceiveResponse(ser, Cmd):
    line = ser.readline()
    text = str(line)        # Convert bytes array to string
		          # 바이트 배열을 문자열로 변환
    if Cmd in text:
        ret = 1
    else:
        ret = -1

    return ret

# ------------------------------------------------------------------------------------------------------
# Function: To send Command and handle response
# 함수: 명령 보내고 반응 다루기
# Inputs:   Ser_Cmd_Str - the serial command string to send
# 들어가는 내용: Ser_Cmd_Str - 보내려는 시리얼 명령문
#           Cmd - the command to send and received
#	 Cmd - 명령을 보내고 받음
#           tic - current time
#	 tic - 현재 시간
#           timeout - time out threshold
#	 시간초과 - 시간 초과 임계값
# return:   ret - -1 = nothing send, -2 = timeout, 1 = command sent, 2 = received reply
# 리턴:   ret - -1 = 보내는 것 없음, -2 = 시간초과, 1 = 명령 보내짐, 2 = 대답 받음
#           Ser_Cmd_Str
#           tic
# ------------------------------------------------------------------------------------------------------
def SerialCommandNResponse(ser, Ser_Cmd_Str, Cmd, tic, timeout):
    ret = -1
    if Ser_Cmd_Str == '':
        Ser_Cmd_Str = Cmd
        SerialSendCommand(ser, Ser_Cmd_Str)
        print('Sent ' + Cmd)
        cur_status = 6
        tic = time.time()
        ret = 1
    else:
        ret2 = SerialReceiveResponse(ser, Ser_Cmd_Str)    # end sure stop command sent and received by micro:bit
        if ret2 == 1:
            Ser_Cmd_Str = ''
            print('Respond')
            ret = 2

        if (time.time() - tic) > timeout: # timeout one second
            Ser_Cmd_Str = ''
            print('Timeout')
            ret = -2

    return ret, Ser_Cmd_Str, tic

# ------------------------------------------------------------------------------------------------------
# Function: Main Program
# 함수: 주요 프로그램
# Inputs:
# 입력:
# return:
# 반환:bug
# ------------------------------------------------------------------------------------------------------
def main():
    # ------------------------------------------------------------------------------------------------------
    # Global Variable intialization
    # 전역 변수 초기화
    # ------------------------------------------------------------------------------------------------------
    Ser_Cmd_Str = ''        # the Serial command string sent to micro:bit
    tic = time.time()       # timeout reference

    # Opening serial port COM25, baud 115200, no parity, no flow control
    ser = serial.Serial('COM5', 115200, timeout=0, parity=serial.PARITY_NONE, rtscts=0)

    Cmd2Send = ''

    print('Input your commands: w, s, a, d, e, q, x')
    # ------------------------------------------------------------------------------------------------------
    # Main Program
    # 주요 프로그램
    # ------------------------------------------------------------------------------------------------------
    while(True):

        if Cmd2Send == '':
            if msvcrt.kbhit():
                key = msvcrt.getch()
                # print('You hit ' + str(key))
                # Handle user keyboard inputs
                if key == b'm':
                    break
                elif key == b'w':
                    Cmd2Send = 'f'
                    print('Forward')
                elif key == b'a':
                    Cmd2Send = 'l'
                    print('Small Left Turn')
                elif key == b'd':
                    Cmd2Send = 'r'
                    print('Small Right Turn')
                elif key == b's':
                    Cmd2Send = 's'
                    print('Stop')
                elif key == b'e':
                    Cmd2Send = 'R'
                    print('Big Right Turn')
                elif key == b'q':
                    Cmd2Send = 'L'
                    print('Big Left Turn')
                elif key == b'x':
                    Cmd2Send = 'B'
                    print('Back')
        else:
            ret, Ser_Cmd_Str, tic = SerialCommandNResponse(ser, Ser_Cmd_Str, Cmd2Send, tic, 2)
            if ret == 2:
                Cmd2Send = ''
                print('Command Done!')



    SerialSendCommand(ser, 's')
    ser.close()

if __name__ == '__main__':
    main()
