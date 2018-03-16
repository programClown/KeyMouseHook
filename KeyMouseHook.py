import os
import time
import re
from pynput import mouse, keyboard
import serial
import serial.tools.list_ports

# NOMAL_KEYS = {"04":"a", "05":"b", "06":"c", "07":"d", "08":"e", "09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j", "0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o", "13":"p", "14":"q", "15":"r", "16":"s", "17":"t", "18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y", "1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4", "22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}
NOMAL_KEYS = {
    "a": '\x04',
    "b": '\x05',
    "c": '\x06',
    "d": '\x07',
    "e": '\x08',
    "f": '\x09',
    "g": '\x0a',
    "h": '\x0b',
    "i": '\x0c',
    "j": '\x0d',
    "k": '\x0e',
    "l": '\x0f',
    "m": '\x10',
    "n": '\x11',
    "o": '\x12',
    "p": '\x13',
    "q": '\x14',
    "r": '\x15',
    "s": '\x16',
    "t": '\x17',
    "u": '\x18',
    "v": '\x19',
    "w": '\x1a',
    "x": '\x1b',
    "y": '\x1c',
    "z": '\x1d',
    "1": '\x1e',
    "2": '\x1f',
    "3": '\x20',
    "4": '\x21',
    "5": '\x22',
    "6": '\x23',
    "7": '\x24',
    "8": '\x25',
    "9": '\x26',
    "0": '\x27',
    keyboard.Key.enter: '\x28',
    keyboard.Key.esc: '\x29',
    keyboard.Key.delete: '\x4c',
    keyboard.Key.backspace: '\x2a',    
    keyboard.Key.tab: '\x2b',
    keyboard.Key.space: '\x2c',
    "-": '\x2d',
    "=": '\x2e',
    "[": '\x2f',
    "]": '\x30',
    "\\": '\x31',
    "`": '\x32',
    ";": '\x33',
    "'": "\x34",
    "<GA>": '\x35',
    ",": '\x36',
    ".": '\x37',
    "/": '\38',
    keyboard.Key.caps_lock: '\x39',
    keyboard.Key.f1: '\x3a',
    keyboard.Key.f2: '\x3b',
    keyboard.Key.f3: '\x3c',
    keyboard.Key.f4: '\x3d',
    keyboard.Key.f5: '\x3e',
    keyboard.Key.f6: '\x3f',
    keyboard.Key.f7: '\x40',
    keyboard.Key.f8: '\x41',
    keyboard.Key.f9: '\x42',
    keyboard.Key.f10: '\x43',
    keyboard.Key.f11: '\x44',
    keyboard.Key.f12: '\x45',
    keyboard.Key.right: '\x4f',
    keyboard.Key.left: '\x50',
    keyboard.Key.down: '\x51',
    keyboard.Key.up: '\x52',
    "*": "\x55",
    "+": "\x57",
    keyboard.Key.ctrl: '\xe0',
    keyboard.Key.shift: '\xe1',
    keyboard.Key.alt: '\xe2',
    keyboard.Key.ctrl_r: '\xe4',
    keyboard.Key.shift_r: '\xe5',
    keyboard.Key.alt_r: '\xe6'
}

# SHIFT_KEYS = {"04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T", "18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y", "1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$", "22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"<RET>","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":"<SPACE>","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":"\"","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>"}


class HIDSerial(object):
    def __init__(self):
        self.port = None

        com_list = []
        port_list = list(serial.tools.list_ports.comports())
        for i, port in enumerate(port_list):
            com_list.append(port[0])
            print(i, ": ", port[0], port[1])
        if com_list == []:
            return
        else:
            num = input("please input which one you want to choose: ")
            if int(num) < len(com_list):
                # 打开端口
                self.port = serial.Serial(
                    port=com_list[int(num)],
                    baudrate=115200,
                    bytesize=8,
                    parity=serial.PARITY_NONE,
                    stopbits=1,
                    timeout=2)
                print(self.port)

    # 发送指令的完整流程
    def send_cmd(self, cmd):
        return self.port.write(cmd)
        # response = self.port.readall()
        # response = self.convert_hex(response)
        # return response

    # 转成16进制的函数
    def convert_hex(self, string):
        res = []
        result = []
        for item in string:
            res.append(item)
        for i in res:
            result.append(hex(i))
        return result


class KeyAndMouseListener(object):
    def __init__(self, port, stop_word=keyboard.Key.esc):
        self.com_port = port
        self.key_listener = None
        self.mouse_listener = None
        self.stop_word = stop_word

    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
            # print(key.char.encode())
            # print(NOMAL_KEYS[key.char])
            self.com_port.send_cmd(NOMAL_KEYS[key.char.lower()].encode())
        except AttributeError:
            print('special key {0} pressed'.format(key))
            if key in NOMAL_KEYS:
                self.com_port.send_cmd(NOMAL_KEYS[key].encode())

    def on_release(self, key):
        print('{0} released'.format(key))
        if key == self.stop_word:
            print('esc is pressed')
            self.key_listener.stop()
            self.mouse_listener.stop()
            self.com_port.port.close()
            return False

    def key_start(self):
        self.key_listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release)
        self.key_listener.start()

    def on_move(self, x, y):
        print('Pointer moved to {0}'.format((x, y)))

    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format('Pressed'
                                  if pressed else 'Released', (x, y)))
        if button == mouse.Button.left:
            print('Left')

        if button == mouse.Button.right:
            print('right')

        if button == mouse.Button.middle:
            print('middle')

    def on_scroll(self, x, y, dx, dy):
        print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

    def mouse_start(self):
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.mouse_listener.start()

    def join(self):
        '''
        join each of key_listener/mouse_listener can run ok, here choose key_listener join.
        '''
        if self.key_listener is not None:
            self.key_listener.join()
        else:
            raise NotImplementedError("key_listener")


def main():
    com_port = HIDSerial()
    if com_port.port is not None:
        key_mouse = KeyAndMouseListener(com_port)
        key_mouse.key_start()
        key_mouse.mouse_start()
        key_mouse.join()
    else:
        print("no com port or com open failed.")


if __name__ == '__main__':
    main()
