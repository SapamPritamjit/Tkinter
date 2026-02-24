import tkinter as tk
import random
import sys
from tkinter import messagebox

# Windows sound support
if sys.platform == "win32":
    import winsound

ROWS = 8
COLS = 8
SIZE = 60
COLORS = ["red", "blue", "green", "yellow", "purple"]

class CandyCrush:
    def __init__(self, root):
        self.root = root
        self.root.title("Candy Crush Deluxe 🍬")
        self.level = 1
        self.score = 0
        self.combo = 0
        self.lives = 5
        self.selected = None

        self.canvas = tk.Canvas(root, width=COLS*SIZE,
                            height=ROWS*SIZE, bg="black")
        self.canvas.pack()

        self.info = tk.Label(root, font=("Arial", 14),
                         bg="black", fg="white")
        self.info.pack(fill="x")

        self.restart_btn = tk.Button(root, text="Restart",
                                    command=self.restart_game,
                                    bg="red", fg="white",
                                    font=("Arial", 12, "bold"))
        self.restart_btn.pack(pady=5)

        self.board = [[self.random_candy() for _ in range(COLS)]
                    for _ in range(ROWS)]

        self.draw_board()
        self.update_info()

        self.canvas.bind("<Button-1>", self.click)
        self.resolve_board()

    def random_candy(self):
        # 10% chance bomb
        if random.random() < 0.1:
            return "bomb"
        return random.choice(COLORS)

    def draw_board(self):
        self.canvas.delete("all")

        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * SIZE
                y1 = r * SIZE
                x2 = x1 + SIZE
                y2 = y1 + SIZE

                color = self.board[r][c]

                if color == "bomb":
                    self.canvas.create_oval(
                        x1+6, y1+6, x2-6, y2-6,
                        fill="white", outline="red", width=3
                    )
                    self.canvas.create_text(
                        x1+SIZE/2, y1+SIZE/2,
                        text="💣", font=("Arial", 18)
                    )
                else:
                    self.canvas.create_oval(
                        x1+6, y1+6, x2-6, y2-6,
                        fill=color, outline="white", width=2
                    )

                    # Gloss effect
                    self.canvas.create_oval(
                        x1+15, y1+15, x1+30, y1+30,
                        fill="white", outline=""
                    )

                if self.selected == (r, c):
                    self.canvas.create_oval(
                        x1+3, y1+3, x2-3, y2-3,
                        outline="gold", width=3
                    )

    def click(self, event):
        col = event.x // SIZE
        row = event.y // SIZE

        if not self.selected:
            self.selected = (row, col)
        else:
            r1, c1 = self.selected
            r2, c2 = row, col

            if abs(r1 - r2) + abs(c1 - c2) == 1:
                self.swap(r1, c1, r2, c2)

                matches = self.find_matches()
                if matches:
                    self.resolve_board()
                else:
                    self.swap(r1, c1, r2, c2)
                    self.lives -= 1

            self.selected = None
            self.update_info()
            self.draw_board()

    def swap(self, r1, c1, r2, c2):
        self.board[r1][c1], self.board[r2][c2] = \
            self.board[r2][c2], self.board[r1][c1]

    def find_matches(self):
        remove = set()

        # Horizontal matches
        for r in range(ROWS):
            count = 1
            for c in range(1, COLS):
                if self.board[r][c] == self.board[r][c-1] and self.board[r][c] is not None:
                    count += 1
                else:
                    if count >= 3:
                        for k in range(count):
                            remove.add((r, c-1-k))
                    count = 1
            if count >= 3:
                for k in range(count):
                    remove.add((r, COLS-1-k))

        # Vertical matches
        for c in range(COLS):
            count = 1
            for r in range(1, ROWS):
                if self.board[r][c] == self.board[r-1][c] and self.board[r][c] is not None:
                    count += 1
                else:
                    if count >= 3:
                        for k in range(count):
                            remove.add((r-1-k, c))
                    count = 1
            if count >= 3:
                for k in range(count):
                    remove.add((ROWS-1-k, c))

        return remove

    def apply_gravity(self):
        for c in range(COLS):
            column = [self.board[r][c] for r in range(ROWS) if self.board[r][c] is not None]
            while len(column) < ROWS:
                column.insert(0, self.random_candy())

            for r in range(ROWS):
                self.board[r][c] = column[r]

        self.animate_fall()

    def animate_fall(self):
        for _ in range(5):
            self.draw_board()
            self.root.update()
            self.root.after(40)

    def update_info(self):
        self.info.config(
            text=f"Score: {self.score}   Level: {self.level}   Lives: {self.lives}   Combo: x{self.combo}"
        )

        if self.lives <= 0:
            self.canvas.unbind("<Button-1>")
            messagebox.showinfo("Game Over 💀", f"Final Score: {self.score}")
            self.info.config(text="GAME OVER 💀")

    def restart_game(self):
        self.level = 1
        self.score = 0
        self.combo = 0
        self.lives = 5
        self.board = [[self.random_candy() for _ in range(COLS)]
                    for _ in range(ROWS)]
        self.canvas.bind("<Button-1>", self.click)
        self.update_info()
        self.draw_board()

    def resolve_board(self):
        while True:
            matches = self.find_matches()

            if not matches:
                break

            self.combo += 1
            points = len(matches) * 10 * self.combo
            self.score += points

            if sys.platform == "win32":
                winsound.Beep(900, 120)

            for r, c in matches:
                self.board[r][c] = None

            self.draw_board()
            self.root.update()
            self.root.after(150)

            self.apply_gravity()

        self.combo = 0


root = tk.Tk()
game = CandyCrush(root)
root.mainloop()