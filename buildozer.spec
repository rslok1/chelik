[app]
title = Gray Game
package.name = graygame
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,json
version = 0.1

requirements = python3==3.10.0,hostpython3==3.10.0,pygame


orientation = landscape
fullscreen = 0

# Версии API
android.api = 34
android.minapi = 24
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True

# Автоматический приём лицензий
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
