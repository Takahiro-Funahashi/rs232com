from queue import Empty
from multiprocessing import freeze_support, set_start_method
from multiprocessing import Process
from multiprocessing import Queue as MP_Queue

import tkinter as tk
from tkinter import ttk
import time

import rs232com as com  # nopep8

COM_PARAM = 'COM_PARAM'
RECV_DATA = 'RECV_DATA'
SEND_DATA = 'SEND_DATA'


class SerialComProcess():
    def __init__(self):
        self.inerval_time = 0.1
        self.instCom = None
        return

    def run(self, hQueue_recv, hQueue_send):
        self.queue_recv, self.queue_send = hQueue_recv, hQueue_send

        self.isLoop = True

        while(self.isLoop):
            self.get_Queue()
            time.sleep(self.inerval_time)

        return

    def get_Queue(self):
        while(not self.queue_recv.empty()):
            item = self.queue_recv.get()
            if COM_PARAM in item:
                param = item[COM_PARAM]

                com_port = param['com_port']
                boudrate = param['boudrate']
                bytesize = param['bytesize']
                stopbits = param['stopbits']
                parity = param['parity']

                self.instCom = com.rs232_com(
                    on_open=self.on_open,
                    on_recv=self.on_recv,
                    on_error=self.on_error,
                    on_close=self.on_close,
                )
                self.inst_comport = self.instCom.open(
                    port=com_port,
                    baudrate=boudrate,
                    bytesize=bytesize,
                    stopbits=stopbits,
                    parity=parity,
                )

            if SEND_DATA in item:
                send_data = item[SEND_DATA]
                if self.instCom:
                    self.instCom.send(send_data)

        if self.instCom:
            self.instCom.recv(is_rep=True)

        return

    def on_open(self, ws, inst_com):
        print("### Open com port ###")

    def on_recv(self, ws, message):
        self.queue_send.put(
            {RECV_DATA: message}
        )

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def join(self):
        self.isLoop = False


class SerialComTool():
    def __init__(self):
        self.isConnect = False
        self.interval_time = 200
        self.inst_comport = None

        self.queue_send, self.queue_recv = MP_Queue(), MP_Queue()

    def create_dialog(self):

        frame_conf = tk.LabelFrame(
            self.dialog,
            text='Serial Configuration'
        )

        frame_1 = tk.Frame(
            frame_conf
        )

        frame_2 = tk.Frame(
            frame_conf
        )

        frame_3 = tk.Frame(
            frame_conf
        )

        label_com = tk.Label(
            frame_1,
            text='COM Port:'
        )

        self.combo_com = ttk.Combobox(
            frame_1,
            values=self.com_ports,
            width=8,
            state='readonly',
        )

        label_boudrate = tk.Label(
            frame_2,
            text='baudrate:'
        )

        self.combo_boudrate = ttk.Combobox(
            frame_2,
            values=com.BAUDRATE_CHOICES,
            width=8,
            state='readonly',
        )
        self.combo_boudrate.current(12)

        label_bytesize = tk.Label(
            frame_2,
            text='bytesize:'
        )

        self.combo_bytesize = ttk.Combobox(
            frame_2,
            values=com.BYTESIZE_CHOICES,
            width=2,
            state='readonly',
        )
        self.combo_bytesize.current(3)

        label_parity = tk.Label(
            frame_2,
            text='parity:'
        )

        self.combo_parity = ttk.Combobox(
            frame_2,
            values=com.PARITY_CHOICES,
            width=6,
            state='readonly',
        )
        self.combo_parity.current(0)

        label_stopbits = tk.Label(
            frame_2,
            text='stopbits:'
        )

        self.combo_stopbits = ttk.Combobox(
            frame_2,
            values=com.STOPBITS_CHOICES,
            width=3,
            state='readonly',
        )
        self.combo_stopbits.current(0)

        self.btn_connect = tk.Button(
            frame_3,
            text='connect',
            width=10,
            command=self.btn_connect_clicked
        )

        frame_send = tk.LabelFrame(
            self.dialog,
            text='Send'
        )

        self.entry_send = tk.Entry(
            frame_send,
            width=89,
        )

        self.btn_send = tk.Button(
            frame_send,
            text='send',
            width=6,
            command=self.btn_send_clicked
        )

        frame_recv = tk.LabelFrame(
            self.dialog,
            text='Recv'
        )

        self.Text_recv = tk.Text(
            frame_recv,
            width=75, height=10
        )

        self.v_scroll = ttk.Scrollbar(
            frame_recv,
            orient=tk.VERTICAL,
            command=self.Text_recv.yview
        )
        self.Text_recv['yscrollcommand'] = self.v_scroll.set

        self.h_scroll = ttk.Scrollbar(
            frame_recv,
            orient=tk.HORIZONTAL,
            command=self.Text_recv.xview
        )
        self.Text_recv['xscrollcommand'] = self.h_scroll.set

        sp = 5
        frame_conf.pack(side=tk.TOP, fill=tk.X, padx=sp, pady=sp)
        frame_1.pack(side=tk.TOP, fill=tk.X, padx=sp, pady=sp)
        frame_2.pack(side=tk.TOP, fill=tk.X, padx=sp, pady=sp)
        frame_3.pack(side=tk.TOP, fill=tk.X, padx=sp, pady=sp)
        label_com.pack(side=tk.LEFT)
        self.combo_com.pack(side=tk.LEFT)
        label_boudrate.pack(side=tk.LEFT)
        self.combo_boudrate.pack(side=tk.LEFT)
        label_bytesize.pack(side=tk.LEFT)
        self.combo_bytesize.pack(side=tk.LEFT)
        label_parity.pack(side=tk.LEFT)
        self.combo_parity.pack(side=tk.LEFT)
        label_stopbits.pack(side=tk.LEFT)
        self.combo_stopbits.pack(side=tk.LEFT)
        self.btn_connect.pack(side=tk.LEFT)

        frame_send.pack(side=tk.TOP, fill=tk.X, padx=sp,
                        pady=sp, ipadx=sp, ipady=sp)
        self.entry_send.pack(side=tk.LEFT)
        self.btn_send.pack(side=tk.LEFT)

        frame_recv.pack(side=tk.TOP, fill=tk.X, padx=sp,
                        pady=sp, ipadx=sp, ipady=sp)
        self.entry_send.pack()
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.Text_recv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.dialog.protocol("WM_DELETE_WINDOW", self.quit)

        return

    def after(self):
        while(not self.queue_recv.empty()):
            item = self.queue_recv.get()
            if RECV_DATA in item:
                message = item[RECV_DATA]
                self.Text_recv.insert(tk.END, message)

        self.after_id = self.dialog.after(self.interval_time, self.after)

    def btn_connect_clicked(self):
        if self.isConnect:
            self.isConnect = False
            self.btn_connect['text'] = 'connect'
            self.close()
        else:
            com_port = self.combo_com.get()
            if com_port in self.com_ports:
                self.open()
                self.isConnect = True
                self.btn_connect['text'] = 'disconnect'

        return

    def btn_send_clicked(self):
        send_data = self.entry_send.get()
        if self.isConnect:
            self.queue_send.put({SEND_DATA: send_data})
        return

    def open(self):
        com_port = self.combo_com.get()
        boudrate = int(self.combo_boudrate.get())
        bytesize = int(self.combo_bytesize.get())
        parity = self.combo_parity.get()
        stopbits = int(self.combo_stopbits.get())

        if com_port in self.com_ports:
            self.instProcess = SerialComProcess()
            self.instComProcess = Process(
                name='SerialComTool',
                target=self.instProcess.run,
                args=(
                    self.queue_send,
                    self.queue_recv,
                )
            )
            self.instComProcess.start()

            set_dict = {
                'com_port': com_port,
                'boudrate': boudrate,
                'bytesize': bytesize,
                'parity': parity,
                'stopbits': stopbits,
            }

            self.queue_send.put({COM_PARAM: set_dict})

            self.isConnect = True

    def close(self):
        # self.instComProcess.join()
        pass

    def quit(self):
        self.dialog.after_cancel(self.after_id)
        self.dialog.quit()

        if self.isConnect:
            self.close()

    def run(self):
        self.com_ports = com.get_port()

        self.dialog = tk.Tk()
        self.dialog.geometry('640x440')
        self.create_dialog()
        self.after_id = self.dialog.after(self.interval_time, self.after)
        self.dialog.mainloop()

        return


if __name__ == '__main__':
    freeze_support()
    set_start_method('spawn')

    instCom = SerialComTool().run()
