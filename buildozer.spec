[app]
title = Gray Game
package.name = graygame
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,jpeg,mp3,json
version = 0.1

# Добавлен openssl — почти всегда нужен в Kivy-проектах
requirements = python3,kivy,openssl

orientation = portrait
fullscreen = 0

# API 34 — ок, но в CI обязательно должен быть установлен platform-tools для API 34
android.api = 34
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a

# Разрешения: если игра не требует особых прав, можно оставить пустым.
# Если есть звук/сеть/камера — добавь через запятую, например: INTERNET,RECORD_AUDIO
android.permissions =

# Для CI важно отключить интерактивные вопросы и ускорить сборку
p4a.source_dir =
p4a.branch = master
p4a.commit =
p4a.targetpython = python3

# NDK и SDK версии: ставь стабильные, которые гарантированно есть в репозиториях
android.ndk_version = 25b
android.sdk_version = 34

# Отключаем лишние логи в CI, чтобы не засорять вывод
buildozer.logfile = buildozer.log
buildozer.warn_on_root = 1
buildozer.log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1

# Профили сборки: можно добавить, если планируешь разные конфигурации
# profile.release =
# profile.debug =
