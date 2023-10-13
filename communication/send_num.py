import bluetooth
def sendNum(data):
    # ESP32의 Bluetooth 주소 (MAC 주소) 입력
    esp32_mac_address = "XX:XX:XX:XX:XX:XX"
    # 블루투스 소켓 생성
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # ESP32와 연결 시도
    try:
        sock.connect((esp32_mac_address, 1))
    except bluetooth.btcommon.BluetoothError as e:
        print("Error:", str(e))
        sock.close()
        exit(1)
    # 숫자 전송
    if data >= 0:
        sock.send(“1\n”)
        sock.send(str(data))
        sock.send(“\n”)
    else:
        sock.send(“0\n”)
        data = -1 * data
        sock.send(str(data))
        sock.send(“\n”)
    # 소켓 닫기
    sock.close()