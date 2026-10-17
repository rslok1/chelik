[app]
title = Chelik Game
package.name = chelik
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,json
version = 1.0.0

# Вместо pygame ставим kivy с проверенным Python 3.10
requirements = python3==3.10.0,hostpython3==3.10.0,kivy==2.3.0

orientation = landscape
fullscreen = 0

# Совпадает с NDK и SDK из вашего рабочего YAML
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
