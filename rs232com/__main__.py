import time

import serial
from serial.tools import list_ports

from ._exceptions import *  # nopep8


BAUDRATE_CHOICES = [
    50, 75, 110, 134, 150, 200, 300, 600,
    1200, 1800, 2400, 4800, 9600,
    19200, 38400, 57600, 115200,
]

BYTESIZE_CHOICES = [
    serial.FIVEBITS,
    serial.SIXBITS,
    serial.SEVENBITS,
    serial.EIGHTBITS,
]

PARITY_CHOICES = [
    serial.PARITY_NAMES[serial.PARITY_NONE],
    serial.PARITY_NAMES[serial.PARITY_EVEN],
    serial.PARITY_NAMES[serial.PARITY_ODD],
]

STOPBITS_CHOICES = [
    serial.STOPBITS_ONE,
    serial.STOPBITS_ONE_POINT_FIVE,
    serial.STOPBITS_TWO,
]

XONXOFF_CHOICES = [
    serial.XON,
    serial.XOFF,
]


def get_port():
    """ シリアルComポートの取得

    Returns:
        [list]: シリアルComポートの文字列
    """

    ports = list_ports.comports()

    com_port = [info.device for info in ports]

    return com_port


class rs232_com():
    def __init__(self,
                 on_open=None, on_recv=None, on_error=None, on_close=None):

        self.is_connect = False
        self.inst_comport = None

        self.on_open = on_open
        self.on_recv = on_recv
        self.on_error = on_error
        self.on_close = on_close

        return

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(self, *args)
            except Exception as e:
                if self.on_error:
                    self.on_error(self, e)

    def _chk_serial_parameter_(self, port: str, **kwargs):
        """ シリアルCOMポートの初期化

        Args:
            port (str): COMポート名
            **kwargs: 以下のkeywordパラメータを指定可能
                "baudrate": ビットレート,
                "bytesize": バイトサイズ(5,6,7,8),
                "parity": パリティ(None,Even,Odd),
                "stopbits": ストップビット指定(1.0/1.5/2.0),
                "xonxoff": (bool)Xon/Xoff制御,
                "rtscts": (bool)RTS/CTS制御,
                "dsrdtr": (bool)DSR/DTR制御,
                "timeout": (float)受信タイムアウト,

        Returns:
            [type]: [description]


        Raises:
            RS232comPortException: port指定の違反
            RS232comArgumentException: オプション指定引数の違反
            RS232comParameterException: オプション指定パラメータの範囲違反

        Returns:
            param(dict): 指定パラメータの辞書

        """
        param_dict = dict()

        parameters = {
            "baudrate": BAUDRATE_CHOICES,
            "bytesize": BYTESIZE_CHOICES,
            "parity": PARITY_CHOICES,
            "stopbits": STOPBITS_CHOICES,
            "xonxoff": [True, False],
            "rtscts": [True, False],
            "dsrdtr": [True, False],
        }

        com_ports = get_port()

        if port not in com_ports:
            raise RS232comPortException(
                "The specified Port is a violation."
            )

        args = list(parameters.keys()) + ['timeout']

        for key in kwargs:
            if key not in args:
                raise RS232comArgumentException(
                    f"{key}:Invalid argument"
                )
            else:
                if key in parameters:
                    param = kwargs[key]
                    param_range = parameters[key]
                    if param not in param_range:
                        raise RS232comParameterException(
                            f'{key}:Invalid parameter.'
                        )
                    else:
                        if key == "xonxoff":
                            if param:
                                param = XONXOFF_CHOICES[0]
                            else:
                                param = XONXOFF_CHOICES[1]

                        param_dict.setdefault(key, param)

                elif key == 'timeout':
                    timeout = kwargs['timeout']
                    if isinstance(timeout, float) or isinstance(timeout, int):
                        if timeout > 0:
                            param_dict.setdefault('timeout', timeout)
                        else:
                            raise RS232comParameterException(
                                f'{key}:Invalid parameter.'
                            )

        if 'timeout' not in param_dict:
            param_dict.setdefault('timeout', 0.3)

        return param_dict

    def open(self, port, **kwargs):
        """ シリアルComポートをOpen

        Raises:
            RS232comOpneException: シリアルポートOpenエラー

        Returns:
            [type]: [description]
        """

        self.port = port

        try:
            param = self._chk_serial_parameter_(port, **kwargs)
        except Exception as e:
            raise RS232comOpneException(f"Error:Serial open error {e}")

        try:
            inst_comport = serial.Serial(self.port)
        except Exception as e:
            raise RS232comOpneException(f"Error:Serial open error {e}")

        if isinstance(param, dict):
            for key, param in param.items():
                if key == "baudrate":
                    inst_comport.baudrate = param
                if key == "bytesize":
                    inst_comport.bytesize = param
                if key == "parity":
                    inst_comport.parity = param[0]
                if key == "stopbits":
                    inst_comport.stopbits = param
                if key == "xonxoff":
                    inst_comport.xonxoff = param
                if key == "rtscts":
                    inst_comport.rtscts = param
                if key == "dsrdtr":
                    inst_comport.dsrdtr = param
                if key == "timeout":
                    inst_comport.timeout = param

        self.is_connect = True
        self.inst_comport = inst_comport

        self._callback(self.on_open, inst_comport)

        return self.inst_comport

    def close(self):
        """ ComポートClose

        Raises:
            RS232comCloseException: シリアルポートCloseエラー

        Returns:
            [bool]: [description]
        """
        try:
            self.inst_comport.close()
        except Exception as e:
            raise RS232comCloseException(f"Error:Serial close error {e}")

        self.is_connect = False
        self.inst_comport = None

        self._callback(self.on_close)

        return True

    def send(self, send_data):
        """ 送信処理

        Args:
            send_data ([type]): [description]

        Raises:
            RS232comValueException: [description]
            RS232comSendException: [description]

        Returns:
            [type]: [description]

        """
        if self.is_connect:
            if isinstance(send_data, bytes):
                pass
            elif isinstance(send_data, str):
                try:
                    send_data = send_data.encode('utf-8')
                except Exception as e:
                    raise RS232comValueException(f"Error:{e}")
            elif isinstance(send_data, int) or isinstance(send_data, float):
                send_data = str(send_data)
                send_data = send_data.encode('utf-8')

            try:
                self.inst_comport.write(send_data)
            except Exception as e:
                raise RS232comSendException(f"Error:{e}")

        else:
            self._callback(
                self.on_error,
                RS232comSendException("Error:RS232C port is not open.")
            )

        return True

    def recv(self, is_rep=False):
        """ 受信処理

        Returns:
            [bytes]: 受信したデータ
        """

        while self.inst_comport.is_open:
            try:
                read_byte = self.inst_comport.read()
            except Exception as e:
                self._callback(self.on_error, e)
            if read_byte:
                self._callback(self.on_recv, read_byte)

            if is_rep:
                break

            time.sleep(0.05)

        return


if __name__ == '__main__':
    def on_open(ws, inst_com):
        print("### Open com port ###")

    def on_recv(ws, message):
        print(message)

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    inst = rs232_com(
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
