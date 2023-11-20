import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, filedialog
import subprocess
import os

class GitBuster:
    def __init__(self, root):
        self.root = root
        self.root.title("GitBuster")
        self.root.geometry('670x400')  # Make sure the window is wide enough for the buttons
        
        self.working_directory = os.getcwd()  # Start with the current working directory
        
        # ScrolledText widget for Git command output
        self.info_text = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD)
        self.info_text.grid(row=8, column=0, columnspan=2, pady=5, padx=5, sticky="nsew")
        
        # Button to select a working directory
        tk.Button(root, text="Select Directory", command=self.select_directory, width=90).grid(row=0, column=0, sticky='ew', padx=5)
        
        # Buttons for Git operations
        tk.Button(root, text="Add Files", command=self.add_files, width=90).grid(row=1, column=0, sticky='ew', padx=5)
        tk.Button(root, text="Commit Changes", command=self.commit_changes, width=90).grid(row=2, column=0, sticky='ew', padx=5)
        tk.Button(root, text="Change Commit Name", command=self.change_commit_name, width=90).grid(row=3, column=0, sticky='ew', padx=5)
        tk.Button(root, text="Push Changes", command=self.push_changes, width=90).grid(row=4, column=0, sticky='ew', padx=5)
        tk.Button(root, text="Change Branch", command=self.change_branch, width=90).grid(row=5, column=0, sticky='ew', padx=5)
        tk.Button(root, text="Create Branch", command=self.create_branch, width=90).grid(row=6, column=0, sticky='ew', padx=5)
        tk.Button(root, text="Git Status", command=self.git_status, width=90).grid(row=7, column=0, sticky='ew', padx=5)

    def run_git_command(self, command):
        try:
            result = subprocess.run(["git"] + command, cwd=self.working_directory, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.info_text.insert(tk.END, f"$ git {' '.join(command)}\n{result.stdout}\n")
        except subprocess.CalledProcessError as e:
            self.info_text.insert(tk.END, f"Error:\n{e.stderr}\n")
        # Autoscroll to the bottom
        self.info_text.see(tk.END)

    def select_directory(self):
        # Open a dialog to select a directory
        directory = filedialog.askdirectory()
        # Update the working directory
        if directory:
            self.working_directory = directory
            self.info_text.insert(tk.END, f"Changed working directory to: {directory}\n")

    def add_files(self):
        add_option = simpledialog.askstring("Input", "Enter 'all' to add all files, or list specific files separated by space:")
        if add_option == 'all':
            self.run_git_command(["add", "."])
        else:
            files_to_add = add_option.split()
            self.run_git_command(["add"] + files_to_add)

    def commit_changes(self):
        commit_message = simpledialog.askstring("Input", "Enter commit message:")
        self.run_git_command(["commit", "-m", commit_message])

    def change_commit_name(self):
        new_name = simpledialog.askstring("Input", "Enter new commit name:")
        self.run_git_command(["commit", "--amend", "-m", new_name])

    def push_changes(self):
        self.run_git_command(["push"])

    def change_branch(self):
        branch_name = simpledialog.askstring("Input", "Enter the name of the branch to checkout:")
        self.run_git_command(["checkout", branch_name])

    def create_branch(self):
        new_branch_name = simpledialog.askstring("Input", "Enter the name of the new branch:")
        self.run_git_command(["checkout", "-b", new_branch_name])

    def git_status(self):
        self.run_git_command(["status"])

# Run the application
if __name__ == '__main__':
    root = tk.Tk()
    app = GitBuster(root)
    root.mainloop()