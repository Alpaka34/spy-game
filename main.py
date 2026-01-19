import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner


CATEGORIES = {
    "Ulaşım Araçları": ["Tren", "Uçak", "Otobüs", "Gemi", "Bisiklet", "Metro", "Tramvay"],
    "Şehirler": ["İstanbul", "Ankara", "Paris", "Roma", "Berlin", "Tokyo", "Londra"],
    "Ülkeler": ["Türkiye", "Fransa", "Almanya", "İtalya", "Japonya", "Kanada"],
    "Nesneler": ["Telefon", "Kalem", "Masa", "Sandalye", "Bilgisayar", "Kitap"]
}


class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.players = None
        self.spies = None
        self.category = None

        layout = BoxLayout(orientation="vertical", spacing=20, padding=40)

        title = Label(text="CASUS OYUNU", font_size=36, size_hint=(1, 0.2))

        self.player_spinner = Spinner(
            text="Oyuncu Sayısı",
            values=[str(i) for i in range(3, 11)],
            size_hint=(1, 0.15)
        )
        self.player_spinner.bind(text=self.set_players)

        self.spy_spinner = Spinner(
            text="Casus Sayısı",
            values=[str(i) for i in range(1, 6)],
            size_hint=(1, 0.15)
        )
        self.spy_spinner.bind(text=self.set_spies)

        self.category_spinner = Spinner(
            text="Kategori",
            values=list(CATEGORIES.keys()),
            size_hint=(1, 0.15)
        )
        self.category_spinner.bind(text=self.set_category)

        self.start_btn = Button(text="OYUNA BAŞLA", size_hint=(1, 0.2))
        self.start_btn.bind(on_press=self.start_game)
        self.start_btn.disabled = True

        layout.add_widget(title)
        layout.add_widget(self.player_spinner)
        layout.add_widget(self.spy_spinner)
        layout.add_widget(self.category_spinner)
        layout.add_widget(self.start_btn)

        self.add_widget(layout)

    def set_players(self, spinner, text):
        self.players = int(text)
        self.update_state()

    def set_spies(self, spinner, text):
        self.spies = int(text)
        self.update_state()

    def set_category(self, spinner, text):
        self.category = text
        self.update_state()

    def update_state(self):
        self.start_btn.disabled = not (
            self.players and self.spies and self.category and self.spies < self.players
        )

    def start_game(self, instance):
        game = self.manager.get_screen("game")
        game.start_round(self.players, self.spies, self.category)
        self.manager.current = "game"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.players = 0
        self.spies = 0
        self.current_player = 1
        self.card_open = False

        # 🔥 YENİ: Kelime havuzu
        self.word_pool = []
        self.last_category = None

        self.layout = BoxLayout(orientation="vertical", spacing=20, padding=40)

        self.info_label = Label(text="", font_size=26)
        self.card_btn = Button(text="KARTI AÇ", font_size=32, size_hint=(1, 0.6))
        self.card_btn.bind(on_press=self.on_card_press)

        self.next_btn = Button(text="YENİ TUR", size_hint=(1, 0.2))
        self.next_btn.bind(on_press=self.go_to_menu)
        self.next_btn.opacity = 0
        self.next_btn.disabled = True

        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.card_btn)
        self.layout.add_widget(self.next_btn)
        self.add_widget(self.layout)

    def start_round(self, players, spies, category):
        self.players = players
        self.spies = spies
        self.category = category
        self.current_player = 1
        self.card_open = False

        # ✅ AYNI KELİME TEKRARINI ENGELLEYEN SİSTEM
        if self.last_category != category or not self.word_pool:
            self.word_pool = CATEGORIES[category].copy()
            random.shuffle(self.word_pool)
            self.last_category = category

        self.keyword = self.word_pool.pop()

        self.spy_players = set(random.sample(range(1, players + 1), spies))

        self.info_label.text = f"Oyuncu {self.current_player} telefonu alsın"
        self.card_btn.text = "KARTI AÇ"
        self.card_btn.disabled = False
        self.next_btn.opacity = 0
        self.next_btn.disabled = True

    def on_card_press(self, instance):
        if not self.card_open:
            if self.current_player in self.spy_players:
                self.card_btn.text = "SEN CASUS'SUN"
            else:
                self.card_btn.text = self.keyword
            self.card_open = True
        else:
            self.card_btn.text = "KARTI AÇ"
            self.card_open = False

            if self.current_player < self.players:
                self.current_player += 1
                self.info_label.text = f"Oyuncu {self.current_player} telefonu alsın"
            else:
                self.card_btn.disabled = True
                self.card_btn.text = "OYUN BAŞLADI"
                self.info_label.text = "Herkes konuşmaya başlasın"
                self.next_btn.opacity = 1
                self.next_btn.disabled = False

    def go_to_menu(self, instance):
        self.manager.current = "setup"


class SpyGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SetupScreen(name="setup"))
        sm.add_widget(GameScreen(name="game"))
        return sm


if __name__ == "__main__":
    SpyGameApp().run()
