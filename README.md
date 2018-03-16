# KeyMouseHook
通过串口把键盘和鼠标消息传递到开发板，开发板通过BLE HID服务模拟鼠标和键盘操作来控制手机的行为

requirements:  
python >= python3.5  
pyserial  
pynput  

test：
NRF52840开发板，固件“ble_app_hids_keyboard_pca10056_s140.hex”，协议栈“s140_nrf52840_5.0.0-2.alpha_softdevice.hex”

run:
step1: NRF52840开发板烧录协议栈和固件，重启，蓝牙开始广播，广播名字“Nordic_Keyboard”
step2: 打开手机系统蓝牙界面，连接“Nordic_Keyboard”设备，确定配对。
step3: 运行 python3 KeyMouseHook.py
step4: 选择串口
  此后，打开手机输入框，发现手机软键盘消失，键盘输入会得到响应

注意：NRF52840重启会擦出bond信息
