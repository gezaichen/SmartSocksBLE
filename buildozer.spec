[app]
title = SmartSocksBLE
package.name = smartsocks
package.domain = org.example
source.dir = .
source.include_exts = py
version = 0.1
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
android.permissions = BLUETOOTH_ADVERTISE,BLUETOOTH_CONNECT
