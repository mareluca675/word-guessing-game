import sys
import tkinter as tk
import random as rand
import guess_data as gs


class WordGuessingGame:
    def __init__(self):
        # Screen settings
        self.screen = tk.Tk()
        self.screen.geometry('1280x780')
        self.screen.title('Word Guessing Game')

        # Initializing screen elements
        self.title = tk.Label(self.screen, text='Welcome to the Word Guessing Game!', font=('Arial', 42))
        self.title.pack(pady=200)  # The title of the main menu
        self.result = tk.Label(self.screen, text='', font=('Arial', 42))
        self.current_word = tk.Label(self.screen, text='', font=('Arial', 42))
        self.guess = tk.Entry(self.screen, font=('Arial', 42), width=20)
        self.exit_button = tk.Button(self.screen, text='Exit', font=('Arial', 30), command=self.exit_game)
        self.submit_button = tk.Button(self.screen, text='Submit', font=('Arial', 42), command=self.submit_guess)
        self.play_again_button = tk.Button(self.screen, text='Play Again', font=('Arial', 35), command=self.start_game)
        self.score_label = tk.Label(self.screen, text='Score: ', font=('Arial', 30))
        self.win_streak_label = tk.Label(self.screen, text='Win streak: ', font=('Arial', 30))

        # Initializing the word to guess and its components
        self.word = ''
        self.guessed_word = []
        self.word_showed = ''
        self.mistakes = 0

        # Initializing the score variable and win streak
        self.score = 0
        self.win_streak = 0

        # Setting up the canvas for drawing the gallow
        self.gallow = tk.Canvas(self.screen, width=300, height=300)

        # Hangman parts
        self.hangman_parts = (
            self.gallow.create_oval(60, 50, 80, 70, width=5, state='disabled'),  # Head
            self.gallow.create_line(70, 110, 70, 70, width=5, state='disabled'),  # Body
            self.gallow.create_line(50, 100, 70, 70, width=5, state='disabled'),  # Left arm
            self.gallow.create_line(90, 100, 70, 70, width=5, state='disabled'),  # Right arm
            self.gallow.create_line(50, 140, 70, 110, width=5, state='disabled'),  # Left leg
            self.gallow.create_line(90, 140, 70, 110, width=5, state='disabled'),  # Right leg
        )

        # Starting the game
        self.start_button = tk.Button(self.screen, text='START', font=('Arial', 40), command=self.start_game)
        self.start_button.pack(pady=100)

    def submit_guess(self):
        answer = self.guess.get().lower()

        if answer == self.word.lower():
            self.current_word.config(text=' '.join(self.word))
            self.screen.after(1500, self.play_again, True)
            return

        if not answer.isalpha() or (answer.isalpha() and len(answer) != 1):
            self.result.config(text="Please enter a single alphabetic character.")
            return

        if gs.checked_letters[answer]:
            self.result.config(text="You've already guessed that letter.")
            return

        gs.checked_letters[answer.lower()] = True  # Marking the letter as checked
        if answer in self.word.lower():
            self.word_showed = ""
            for index, letter in enumerate(self.word):
                if not letter == ' ':
                    if letter.lower() == answer or gs.checked_letters[letter.lower()]:
                        self.guessed_word[index] = letter
                        self.word_showed += letter + ' '
                    else:
                        self.guessed_word[index] = '_'
                        self.word_showed += '_ '
                else:
                    self.guessed_word[index] = ' '
                    self.word_showed += ' '
            self.current_word.config(text=self.word_showed)
        else:
            self.result.config(text="The letter isn't in the word.")
            self.mistake()

        if '_' not in self.guessed_word:
            self.current_word.config(text=' '.join(self.word))
            self.result.after(1000, self.play_again, True)
            return

    def start_game(self):
        # Removing the start button
        self.start_button.pack_forget()

        # Resetting the play again button
        self.play_again_button.pack_forget()

        # Resetting the hangman parts
        self.mistakes = 0
        for index, _ in enumerate(self.hangman_parts):
            self.gallow.itemconfig(self.hangman_parts[index], state='hidden')

        # Resetting the dictionary
        gs.checked_letters = {key: gs.default_value for key in gs.checked_letters}

        # Title
        self.title.config(text="Can you guess the word?", font=('Arial', 42))
        self.title.pack(pady=20)

        # Result label
        self.result.config(text="", font=('Arial', 42))
        self.result.pack(pady=20)

        # Current progress done in guessing the word
        self.current_word.pack(pady=60)

        # Input
        self.guess.pack(pady=40)

        # Score and win streak
        self.score_label.place(x=10, y=10)
        self.win_streak_label.place(x=10, y=50)
        self.score_label.config(text=f"Score: {self.score}", font=('Arial', 30))
        self.win_streak_label.config(text=f"Win streak: {self.win_streak}", font=('Arial', 30))

        # Exit button
        self.exit_button.place(x=50, y=650)

        # Submit button
        self.submit_button.pack(pady=20)

        # Gallow
        self.gallow.place(x=970, y=240)
        self.gallow.create_line(50, 250, 250, 250, width=5)  # Base
        self.gallow.create_line(150, 0, 150, 250, width=5)  # Pole
        self.gallow.create_line(70, 0, 150, 0, width=15)  # Hanging Stick 1
        self.gallow.create_line(70, 50, 70, 0, width=5)  # Hanging Stick 2

        # Getting the word
        self.word = rand.choice(gs.words)
        print(self.word)

        # Generating the to be guessed word
        self.guessed_word = ['_' for _ in self.word]

        # Defining a string with the word that shows on the screen
        self.word_showed = ''
        for letter in self.word:
            if not letter == ' ':
                self.word_showed += '_ '
            else:
                self.word_showed += ' '

        # Showing the current progress
        self.current_word.config(text=self.word_showed)

    def play_again(self, won, cheat=False):
        # Removing unwanted items
        self.title.config(text='')
        self.submit_button.pack_forget()
        self.guess.pack_forget()
        self.gallow.place_forget()

        if cheat:  # Cheatcode :)
            self.result.config(text="You found the cheatcode!")
            self.current_word.config(text="69")
        else:
            if won:
                self.result.config(text="You guessed the word!")
                self.score += 10 + 10 * self.win_streak
                self.win_streak += 1
            else:
                self.result.config(text="You lost and died!")
                self.score = 0
                self.win_streak = 0

            # Displaying the play again button
            self.play_again_button.pack(pady=50)

            # Moving the exit button to the middle of the screen
            self.exit_button.pack(pady=20)

            # Revealing the word
            self.current_word.config(text=f"The word was {self.word}.")

    def mistake(self):
        self.mistakes += 1
        self.result.config(text="The letter isn't in the word.")

        # Changing the state of one of the hangman parts to make it visible
        self.gallow.itemconfig(self.hangman_parts[self.mistakes - 1], state='normal')

        if self.mistakes == len(self.hangman_parts):
            self.screen.after(1500, self.play_again, False)
            return

    def exit_game(self):
        # Removing all the buttons/labels from the screen
        self.win_streak_label.place_forget()
        self.score_label.place_forget()
        self.title.pack_forget()
        self.submit_button.pack_forget()
        self.guess.pack_forget()
        self.gallow.place_forget()
        self.current_word.pack_forget()
        self.exit_button.pack_forget()
        self.play_again_button.pack_forget()

        # Displaying a goodbye message
        self.result.place(x=395, y=320)
        self.result.config(text='Thanks for playing!')
        self.result.after(1500, sys.exit)


WordGuessingGame().screen.mainloop()
