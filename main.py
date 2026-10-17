import os
import math
import random
import json

# Игнорируем лишние аргументы командной строки Kivy
os.environ['KIVY_NO_ARGS'] = '1'

# Устанавливаем альбомную (горизонтальную) ориентацию окна до загрузки графического контекста
from kivy.config import Config
Config.set('graphics', 'orientation', 'landscape')

from kivy.core.window import Window
# Фиксируем альбомную ориентацию на устройствах
try:
    Window.orientation = 'landscape'
except Exception:
    pass

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

SAVE_FILE = "progress.json"

# ==========================================
# 🎵 СПИСОК МУЗЫКИ
# ==========================================
TRACKS = [
    {"id": "track1", "name": "Веселая", "file": "1.mp3"},
    {"id": "track2", "name": "Спокойная", "file": "2.mp3"},
    {"id": "track3", "name": "Интрига", "file": "3.mp3"},
    {"id": "off", "name": "Выключить музыку", "file": None}
]

MUSIC_ICON_FILE = "music_icon.png"

# ==========================================
# ЕДИНСТВЕННЫЙ СКИН
# ==========================================
PLAYER_SKIN = {
    "name": "Герой",
    "color": (1, 1, 1, 1),
    "image": "chel1.png"
}


def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"max_level": 1, "music_id": "track1"}


def save_data(max_lvl, music_id):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"max_level": max_lvl, "music_id": music_id}, f, ensure_ascii=False)
    except Exception:
        pass


# ------------------------------------------
# ЭКРАН ВЫБОРА УРОВНЕЙ И ВЕРХНЕЕ МЕНЮ
# ------------------------------------------
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')

        # --- САМАЯ ВЕРХНЯЯ СЕКЦИЯ: Кнопка музыки по центру (адаптирована под альбомный экран) ---
        top_music_box = BoxLayout(size_hint_y=0.14, padding=[10, 4, 10, 4])

        self.music_btn = Button(
            text="МУЗЫКА",
            size_hint=(0.3, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_color=(0.15, 0.25, 0.35, 1),
            bold=True
        )

        if os.path.exists(MUSIC_ICON_FILE):
            try:
                self.music_btn.text = ""
                self.music_btn.background_normal = MUSIC_ICON_FILE
            except Exception:
                pass

        self.music_btn.bind(on_release=self.open_music_popup)

        top_music_box.add_widget(Widget(size_hint_x=0.35))
        top_music_box.add_widget(self.music_btn)
        top_music_box.add_widget(Widget(size_hint_x=0.35))

        self.main_layout.add_widget(top_music_box)

        # --- ВТОРАЯ СЕКЦИЯ: Заголовок ---
        top_bar = BoxLayout(size_hint_y=0.11, padding=[10, 2, 10, 2])

        title_btn = Button(
            text="СЕРЫЙ ПУТЬ (100 Ур.)",
            disabled=True,
            background_color=(0.12, 0.12, 0.16, 1),
            color=(1, 1, 1, 1)
        )

        top_bar.add_widget(title_btn)
        self.main_layout.add_widget(top_bar)

        # --- СЕТКА СО 100 УРОВНЯМИ (для горизонтального экрана 8 колонок удобнее) ---
        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.grid = GridLayout(cols=8, spacing=8, padding=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.scroll.add_widget(self.grid)
        self.main_layout.add_widget(self.scroll)
        self.add_widget(self.main_layout)

    def on_enter(self):
        self.update_grid()

    def update_grid(self):
        self.grid.clear_widgets()
        app = App.get_running_app()
        max_lvl = app.max_unlocked if app else 1

        for i in range(1, 101):
            unlocked = i <= max_lvl
            btn = Button(
                text=str(i) if unlocked else "",
                size_hint_y=None,
                height=65,
                font_size=16,
                bold=True,
                background_color=(0.2, 0.7, 0.3, 1) if unlocked else (0.25, 0.25, 0.25, 1),
                color=(1, 1, 1, 1) if unlocked else (0.5, 0.5, 0.5, 1),
                disabled=not unlocked
            )
            btn.bind(on_release=lambda x, l=i: self.start_game(l))
            self.grid.add_widget(btn)

    def start_game(self, level):
        self.manager.get_screen('game').setup(level)
        self.manager.current = 'game'

    def open_music_popup(self, instance):
        app = App.get_running_app()
        content = BoxLayout(orientation='vertical', spacing=8, padding=10)

        for tr in TRACKS:
            is_selected = (tr['id'] == app.current_music_id)
            btn_text = f"{tr['name']}" + ("  [АКТИВНО]" if is_selected else "")

            m_btn = Button(
                text=btn_text,
                size_hint_y=None,
                height=48,
                background_color=(0.2, 0.6, 0.4, 1) if is_selected else (0.25, 0.25, 0.3, 1)
            )

            def select_track(inst, track_id=tr['id']):
                app.set_music(track_id)
                popup.dismiss()

            m_btn.bind(on_release=select_track)
            content.add_widget(m_btn)

        popup = Popup(title="Выберите фоновую музыку", content=content, size_hint=(0.6, 0.75), auto_dismiss=True)
        popup.open()


# ------------------------------------------
# ИГРОВОЙ ВИДДЖЕТ (ГЕЙМПЛЕЙ)
# ------------------------------------------
class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = 1
        self.player_pos = [400, 400]
        self.target_pos = [0, 0]
        self.world_size = 1000
        self.speed = 6.5
        self.touch_target = None

        self.player_size = 100
        with self.canvas:
            self.bg_color = Color(0.22, 0.22, 0.24, 1)
            self.bg_rect = Rectangle()

            self.target_color = Color(0.23, 0.23, 0.25, 1)
            self.target_ent = Ellipse(size=(16, 16))

            self.player_color = Color(1, 1, 1, 1)
            self.player_rect = Rectangle(size=(self.player_size, self.player_size))

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def setup(self, level):
        self.level = level

        self.world_size = 1000 + (level - 1) * 140
        self.player_pos = [self.world_size / 2, self.world_size / 2]

        self.target_pos = [
            random.randint(100, max(105, int(self.world_size - 100))),
            random.randint(100, max(105, int(self.world_size - 100)))
        ]

        diff = max(0.003, 0.025 - (level * 0.0002))
        self.target_color.rgb = (0.22 + diff, 0.22 + diff, 0.24 + diff)

        # Автоматическая установка единственного скина
        if PLAYER_SKIN['image'] and os.path.exists(PLAYER_SKIN['image']):
            self.player_rect.source = PLAYER_SKIN['image']
            self.player_color.rgb = (1, 1, 1)
        else:
            self.player_rect.source = ''
            self.player_color.rgba = PLAYER_SKIN['color']

        self.touch_target = None

    def on_touch_down(self, touch):
        self.touch_target = touch.pos
        offset_x = self.width / 2 - self.player_pos[0]
        offset_y = self.height / 2 - self.player_pos[1]
        tx = self.target_pos[0] + offset_x
        ty = self.target_pos[1] + offset_y

        if math.dist(touch.pos, (tx, ty)) < 45:
            app = App.get_running_app()
            if app:
                app.complete_level(self.level)

    def on_touch_move(self, touch):
        self.touch_target = touch.pos

    def on_touch_up(self, touch):
        self.touch_target = None

    def update(self, dt):
        if self.touch_target:
            dx = self.touch_target[0] - self.width / 2
            dy = self.touch_target[1] - self.height / 2
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist > 6:
                self.player_pos[0] += (dx / dist) * self.speed
                self.player_pos[1] += (dy / dist) * self.speed

                self.player_pos[0] = max(0, min(self.world_size, self.player_pos[0]))
                self.player_pos[1] = max(0, min(self.world_size, self.player_pos[1]))

        offset_x = self.width / 2 - self.player_pos[0]
        offset_y = self.height / 2 - self.player_pos[1]

        self.bg_rect.pos = (offset_x, offset_y)
        self.bg_rect.size = (self.world_size, self.world_size)

        self.target_ent.pos = (offset_x + self.target_pos[0], offset_y + self.target_pos[1])

        half = self.player_size / 2
        self.player_rect.pos = (self.width / 2 - half, self.height / 2 - half)


class GameScreen(Screen):
    def setup(self, level):
        self.game.setup(level)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = GameWidget()
        self.add_widget(self.game)

        back = Button(
            text="Меню",
            size_hint=(0.16, 0.12),
            pos_hint={'x': 0.02, 'y': 0.85},
            background_color=(0.2, 0.2, 0.2, 0.8)
        )
        back.bind(on_release=self.go_back)
        self.add_widget(back)

    def go_back(self, instance):
        self.manager.current = 'menu'


class MainApp(App):
    def build(self):
        data = load_data()
        self.max_unlocked = data.get("max_level", 1)
        self.current_music_id = data.get("music_id", "track1")

        self.current_sound = None
        self.play_current_music()

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

    def set_music(self, track_id):
        self.current_music_id = track_id
        save_data(self.max_unlocked, self.current_music_id)
        self.play_current_music()

    def play_current_music(self):
        try:
            if self.current_sound:
                self.current_sound.stop()
                self.current_sound = None

            track_data = next((t for t in TRACKS if t['id'] == self.current_music_id), None)
            if track_data and track_data['file']:
                file_path = track_data['file']
                if os.path.exists(file_path):
                    self.current_sound = SoundLoader.load(file_path)
                    if self.current_sound:
                        self.current_sound.loop = True
                        self.current_sound.play()
        except Exception as e:
            print(f"Ошибка воспроизведения звука: {e}")

    def complete_level(self, completed_lvl):
        if completed_lvl == self.max_unlocked and completed_lvl < 100:
            self.max_unlocked += 1
            save_data(self.max_unlocked, self.current_music_id)
        self.root.current = 'menu'


if __name__ == "__main__":
    MainApp().run()
