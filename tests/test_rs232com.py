
import os
import sys

parent_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(parent_path)
if True:
    import rs232com as com


if __name__ == '__main__':
    def on_open(ws, inst_com):
        print("### Open com port ###")

    def on_recv(ws, message):
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    inst = com.rs232_com(
        on_open=on_open,
        on_recv=on_recv,
        on_error=on_error,
        on_close=on_close,
    )

    inst.open(
        port="COM4",
        baudrate=9600,
        bytesize=8,
        parity='None',
        stopbits=1,
    )

    inst.send(
        'COM4 open!!'
    )

    inst.recv()
