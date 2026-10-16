[app]
title = Chelik
package.name = chelik
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,json
version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Важно: согласовано с тем, что ставится в workflow (platforms;android-34)
android.api = 34
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.permissions =

[buildozer]
log_level = 2
warn_on_root = 1
