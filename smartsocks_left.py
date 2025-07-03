# main.py - SmartSocks_Left BLE 模拟器

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import time
import numpy as np
import struct

from jnius import autoclass, cast
from android import activity
from android.permissions import request_permissions, Permission

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothManager = autoclass('android.bluetooth.BluetoothManager')
BluetoothGattCharacteristic = autoclass('android.bluetooth.BluetoothGattCharacteristic')
BluetoothGattService = autoclass('android.bluetooth.BluetoothGattService')
UUID = autoclass('java.util.UUID')

class BLESimulator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.btn_start = Button(text='开始模拟')
        self.btn_stop = Button(text='停止模拟')
        self.add_widget(self.btn_start)
        self.add_widget(self.btn_stop)

        self.btn_start.bind(on_press=self.start_simulation)
        self.btn_stop.bind(on_press=self.stop_simulation)

        self.sim_event = None
        self.frame_id = 0
        self.bt_manager = None
        self.bt_adapter = None
        self.bt_service = None
        self.bt_characteristic = None

        request_permissions([Permission.BLUETOOTH_ADVERTISE, Permission.BLUETOOTH_CONNECT])

    def start_simulation(self, *args):
        self.frame_id = 0
        self.setup_ble()
        self.sim_event = Clock.schedule_interval(self.send_packet, 1 / 60.0)

    def stop_simulation(self, *args):
        if self.sim_event:
            self.sim_event.cancel()
            self.sim_event = None

    def setup_ble(self):
        Context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.bt_manager = cast('android.bluetooth.BluetoothManager', Context.getSystemService(Context.BLUETOOTH_SERVICE))
        self.bt_adapter = self.bt_manager.getAdapter()
        self.bt_adapter.setName("SmartSocks_Left")
        self.bt_adapter.setEnabled(True)

        self.bt_service = BluetoothGattService(UUID.fromString("0000ffe0-0000-1000-8000-00805f9b34fb"), BluetoothGattService.SERVICE_TYPE_PRIMARY)
        self.bt_characteristic = BluetoothGattCharacteristic(
            UUID.fromString("0000ffe1-0000-1000-8000-00805f9b34fb"),
            BluetoothGattCharacteristic.PROPERTY_NOTIFY,
            BluetoothGattCharacteristic.PERMISSION_READ
        )
        self.bt_service.addCharacteristic(self.bt_characteristic)
        # 模拟服务逻辑需要在 Java 层注册 GATT Server，这里仅保留接口结构

    def send_packet(self, dt):
        self.frame_id += 1
        timestamp = time.time()
        pressure = np.random.randint(0, 1000, size=512, dtype=np.uint16)
        imu = np.random.randn(12).astype(np.float32)  # 模拟 IMU 12 维

        packet = struct.pack("<Hf", self.frame_id, timestamp) + pressure.tobytes() + imu.tobytes()

        # ⚠️ 实际模拟 BLE notify 的部分略过，仅记录调试输出
        print(f"[发送] 帧号: {self.frame_id}, 时间戳: {timestamp}, 压力均值: {pressure.mean():.2f}")
        # self.bt_characteristic.setValue(packet)  # BLE 模拟 GATT Server 需要 Java 层注册

class SmartSocksApp(App):
    def build(self):
        return BLESimulator()

if __name__ == '__main__':
    SmartSocksApp().run()
