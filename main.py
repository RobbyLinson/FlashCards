import os
import tkinter as tk
import random
import json
from tkinter import messagebox

# Function to load flashcards from a JSON file
def load_flashcards(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Start the flashcard GUI with a given flashcard set
def start_flashcards(flashcard_set):
    global flashcards, current_index, root
    flashcards = load_flashcards(flashcard_set)
    random.shuffle(flashcards)
    current_index = 0
    root.destroy()  # Close the home screen window
    display_flashcards_gui()  # Open the flashcards display

# Function to display the flashcard GUI
def display_flashcards_gui():
    global root, question_label, answer_label, flashcards, current_index
    root = tk.Tk()
    root.title("Flashcard App")
    root.geometry("800x600")

    # Function to go to the next card
    def next_card(event=None):
        global current_index
        current_index = (current_index + 1) % len(flashcards)
        update_card()

    # Function to go to the previous card
    def prev_card(event=None):
        global current_index
        current_index = (current_index - 1) % len(flashcards)
        update_card()

    # Function to shuffle the flashcards
    def shuffle_flashcards():
        global current_index
        random.shuffle(flashcards)
        current_index = 0
        update_card()

    # Function to update the displayed card
    def update_card():
        global question_label, answer_label
        card = flashcards[current_index]
        question_label.config(text=card['term'])
        answer_label.config(text="")

    # Function to reveal the answer to the current card
    def reveal_answer(event=None):
        global answer_label
        answer_label.config(text=flashcards[current_index]['definition'], fg='red')

    # Bind keys
    root.bind("<space>", reveal_answer)
    root.bind("<Right>", next_card)
    root.bind("<Left>", prev_card)

    # GUI setup
    question_label = tk.Label(root, text="", font=('Arial', 24), pady=20, wraplength=400)
    question_label.pack()

    answer_label = tk.Label(root, text="", font=('Arial', 20), pady=20, wraplength=400)
    answer_label.pack()

    # Navigation frame for the buttons
    navigation_frame = tk.Frame(root)
    navigation_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    # Frame for the Show Answer button
    answer_frame = tk.Frame(root)
    answer_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

    # Navigation buttons
    prev_card_button = tk.Button(navigation_frame, text="← Prev", command=prev_card)
    prev_card_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    shuffle_button = tk.Button(navigation_frame, text="Shuffle", command=shuffle_flashcards)
    shuffle_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    next_card_button = tk.Button(navigation_frame, text="Next →", command=next_card)
    next_card_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Show Answer button, placed in the navigation frame alongside the others
    show_answer_button = tk.Button(answer_frame, text="Show Answer\n(Space)", command=reveal_answer)
    show_answer_button.pack(side=tk.LEFT, fill=tk.X, expand=True)


    shuffle_flashcards()  # Initially shuffle the flashcards
    update_card()  # Display the first card

    # Start the GUI
    root.mainloop()

# Initialize the home GUI
def initialize_gui():
    global root
    root = tk.Tk()
    root.title("Flashcard App Home")
    root.geometry("800x600")

    # Create a Listbox to display the flashcard sets
    listbox = tk.Listbox(root)
    listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Get a list of flashcard JSON files
    flashcard_sets = [f for f in os.listdir('.') if f.endswith('.json')]

    # Insert the flashcard sets into the Listbox
    for flashcard_set in flashcard_sets:
        listbox.insert(tk.END, flashcard_set)

    # Function to handle the selection of a flashcard set
    def select_flashcard_set():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a flashcard set.")
            return
        selected_set = listbox.get(selection[0])
        start_flashcards(selected_set)

    # Create a Select button to load the chosen flashcard set
    select_button = tk.Button(root, text="Select Flashcard Set", command=select_flashcard_set)
    select_button.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    initialize_gui()