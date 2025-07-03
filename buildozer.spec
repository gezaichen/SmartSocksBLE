[app]
title = SmartSocksBLE
package.name = smartsocks
package.domain = org.example
source.dir = .
source.include_exts = py
source.include_patterns = smartsocks_left.py
version = 0.1
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

# ✅ Android 配置（避免 SDK License 报错）
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.accept_sdk_license = True

# ✅ Android 权限（BLE 需要）
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_CONNECT,BLUETOOTH_ADVERTISE

# ✅ 编译输出控制（可选）
copy_libs = 1
