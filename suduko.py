import tkinter as tk
import random
from tkinter import messagebox

class SudokuGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.create_widgets()
        self.generate_puzzle()
        self.update_entries()

    def create_widgets(self):
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.entries[i][j] = tk.Entry(self.master, width=3, font=('Helvetica', 16), justify='center')
                self.entries[i][j].grid(row=i, column=j)
                
                if (i in (2, 5) and j % 3 == 0) or (i % 3 == 0 and j in (2, 5)):
                    self.entries[i][j].config(highlightthickness=5)  # Add extra padding to thicker lines
                elif (i % 3 == 0 and j % 3 == 0):
                    self.entries[i][j].config(highlightthickness=2)  # Add extra padding to thicker lines

        check_button = tk.Button(self.master, text="Check Solution", command=self.check_solution)
        check_button.grid(row=9, columnspan=9)

        solve_button = tk.Button(self.master, text="Solve", command=self.solve_puzzle_wrapper)
        solve_button.grid(row=10, columnspan=9)

        new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        new_game_button.grid(row=11, columnspan=9)

    def generate_puzzle(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_puzzle()  # Generate a complete valid Sudoku puzzle
        self.remove_numbers()  # Remove some numbers to create the initial puzzle

    def solve_puzzle_wrapper(self):
        solved = self.solve_puzzle()
        if solved:
            self.update_entries()
            messagebox.showinfo("Solved", "Sudoku puzzle solved!")
        else:
            messagebox.showerror("Unsolvable", "This Sudoku puzzle is unsolvable!")

    def solve_puzzle(self):
        board_copy = [row[:] for row in self.board]
        solved = solve_sudoku(board_copy)
        if solved:
            self.board = board_copy
        return solved

    def remove_numbers(self):
        for _ in range(45):  # Remove 45 numbers from the complete puzzle
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def check_solution(self):
        self.board = [[0 if self.entries[i][j].get() == '' else int(self.entries[i][j].get()) for j in range(9)] for i in range(9)]
        if self.is_valid_solution():
            messagebox.showinfo("Congratulations", "Congratulations! You solved the Sudoku puzzle!")
        else:
            messagebox.showerror("Incorrect", "Sorry, the solution is incorrect. Please try again.")

    def is_valid_solution(self):
        for i in range(9):
            row_set = set()
            col_set = set()
            for j in range(9):
                if self.board[i][j] in row_set or self.board[j][i] in col_set:
                    return False
                row_set.add(self.board[i][j])
                col_set.add(self.board[j][i])

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                grid_set = set()
                for k in range(3):
                    for l in range(3):
                        if self.board[i+k][j+l] in grid_set:
                            return False
                        grid_set.add(self.board[i+k][j+l])

        return True

    def is_valid_move(self, row, col, num):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def update_entries(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(tk.END, self.board[i][j])
                    self.entries[i][j].config(state='disabled')
                else:
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].config(state='normal')

    def new_game(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state='normal')
                self.entries[i][j].delete(0, tk.END)
        self.generate_puzzle()
        self.update_entries()

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid_move(board, row, col, num):
    return (not used_in_row(board, row, num) and 
            not used_in_col(board, col, num) and 
            not used_in_box(board, row - row % 3, col - col % 3, num))

def used_in_row(board, row, num):
    return num in board[row]

def used_in_col(board, col, num):
    return any(board[i][col] == num for i in range(9))

def used_in_box(board, start_row, start_col, num):
    return any(board[start_row + i][start_col + j] == num for i in range(3) for j in range(3))

def main():
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
