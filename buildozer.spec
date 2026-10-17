[app]
title = Gray Game
package.name = graygame
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,json
version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.permissions =

[buildozer]
log_level = 2
warn_on_root = 1
