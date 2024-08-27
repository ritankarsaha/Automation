import re
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import ssl
import nltk
from nltk.corpus import words

# Fix SSL certificate issue
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("words")

class SpellingChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Spelling Checker")
        self.root.geometry("600x500")

        self.text = ScrolledText(self.root, font=("Arial", 14), wrap=tk.WORD)
        self.text.bind("<KeyRelease>", self.check_spelling)
        self.text.pack(expand=True, fill=tk.BOTH)
        self.old_spaces = 0

        self.root.mainloop()

    def check_spelling(self, event):
        content = self.text.get("1.0", tk.END).strip()
        space_count = content.count(" ")

        if space_count != self.old_spaces:
            self.old_spaces = space_count

            # Clear existing tags
            for tag in self.text.tag_names():
                self.text.tag_delete(tag)

            # Check each word and highlight if incorrect
            words_in_text = content.split(" ")
            for word in words_in_text:
                clean_word = re.sub(r"[^\w]", "", word.lower())
                if clean_word and clean_word not in words.words():
                    start_idx = content.find(word)
                    end_idx = start_idx + len(word)
                    self.text.tag_add(clean_word, f"1.{start_idx}", f"1.{end_idx}")
                    self.text.tag_config(clean_word, foreground="red")

if __name__ == "__main__":
    SpellingChecker()
