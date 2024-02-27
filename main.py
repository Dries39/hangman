from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase

class HangmanGame(BoxLayout):
    def __init__(self, **kwargs):
        super(HangmanGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.replay_button = Button(
            text="Replay",
            on_press=self.replay_game,
            size_hint=(None, None),
            size=(120, 60),
            pos_hint={'center_x': 0.1, 'center_y': 0.1},
        )
        self.replay_button.disabled = True  # Disable replay button initially
        self.add_widget(self.replay_button)

        # Set background color
        with self.canvas.before:
            Color(0.96, 0.91, 0.84, 1)  # Beige color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Add a line of spacing above "STA OPEN"
        self.word_to_guess = ["STA OPEN VOOR HET ONVERWACHTE"]  # Single line for the word to guess
        self.guessed_letters = set()
        self.incorrect_guesses = 0  # Count of incorrect guesses

        # Display hangman image with a slightly decreased size
        self.hangman_image = Image(source=f'hangman{self.incorrect_guesses}.png', size_hint_y=None, height=480)  # Decreased height
        self.add_widget(self.hangman_image)

        # Set the font size for both word guess and letter buttons
        word_label_font_size = '64sp'  # Increased font size for the word label
        button_font_size = '48sp'  # Font size for the letter buttons

        # Add word to guess label with increased font size and central alignment
        self.word_label = Label(
            text=self.display_word(),
            font_size=word_label_font_size,
            color=(1, 0, 0, 1),
            font_name='christmaseve',
            halign='center',  # Center alignment
            valign='middle',  # Middle vertical alignment
            pos_hint={'center_y': 0.3}  # Adjusted position
        )
        self.add_widget(self.word_label)

        # Add buttons for each letter in two rows with slightly smaller squares
        letters_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=400, pos_hint={'center_x': 0.55})  # Adjusted position

        for i in range(2):
            row_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), height=180)
            letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i * 13: (i + 1) * 13]
            for letter in letters:
                btn = Button(
                    text=letter,
                    on_press=self.guess_letter,
                    size_hint=(None, None),
                    size=(120, 120),  # Slightly smaller size
                    font_size=button_font_size,  # Set the font size for the buttons
                    font_name='christmaseve',  # Set the font for the buttons
                    background_color=(1, 0, 0, 1),  # Red background color
                    color=(1, 0.84, 0, 1)  # Gold font color
                )
                row_layout.add_widget(btn)
            letters_layout.add_widget(row_layout)

        self.add_widget(letters_layout)

    def display_word(self):
        display = ""
        for line in self.word_to_guess:
            for letter in line:
                if letter in self.guessed_letters or letter == " ":
                    display += letter
                else:
                    display += "_"
        return display

    def guess_letter(self, instance):
        letter = instance.text
        if letter not in self.guessed_letters:
            self.guessed_letters.add(letter)
            self.word_label.text = self.display_word()

            if all(char in self.guessed_letters or char == " " for char in "".join(self.word_to_guess)):
                self.word_label.text = "STA OPEN VOOR HET ONVERWACHTE"
                self.replay_button.disabled = False  # Enable replay button
                self.hangman_image.source = 'hangman7.png'  # Change to hangman7.png on win
                return  # Return to exit the method if the word is guessed

            # Update hangman image only if the guessed letter is incorrect
            if letter not in "".join(self.word_to_guess):
                self.incorrect_guesses += 1
                if self.incorrect_guesses <= 5:
                    self.hangman_image.source = f'hangman{self.incorrect_guesses}.png'
                else:
                    self.hangman_image.source = f'hangman6.png'
                    self.word_label.text = "Game Over!"
                    self.replay_button.disabled = False  # Enable replay button

    def replay_game(self, instance):
        # Reset game state
        self.word_to_guess = ["STA OPEN VOOR HET ONVERWACHTE"]
        self.guessed_letters = set()
        self.incorrect_guesses = 0

        # Reset UI elements
        self.word_label.text = self.display_word()
        self.hangman_image.source = f'hangman{self.incorrect_guesses}.png'

        # Disable replay button after starting a new game
        self.replay_button.disabled = True

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class HangmanApp(App):
    def build(self):
        LabelBase.register(name='christmaseve', fn_regular='christmaseve.ttf')
        return HangmanGame()

if __name__ == '__main__':
    HangmanApp().run()