[app]
title = Gray Game
package.name = graygame
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,json
version = 0.1

requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

# Версии API
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Автоматический приём лицензий
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
