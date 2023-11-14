import tkinter as tk
from tkinter import ttk
from collections import deque

class PageReplacementSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Page Replacement Simulator")
        self.master.geometry("640x450")  # Set the initial size of the window

        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a classic theme

        # Set the background color for the entire window
        self.master.configure(bg="#000000")

        # Configure other styles
        self.style.configure("TFrame", background="#000000")
        self.style.configure("TButton", background="#404040", foreground="#FFFFFF", font=("Segoe UI", 15, "bold"))
        self.style.configure("TLabel", background="#000000", foreground="#FFFFFF", font=("Segoe UI", 15))
        self.style.configure("TEntry", fieldbackground="#404040", foreground="#FFFFFF", font=("Segoe UI", 15))
        self.style.configure("TCombobox", fieldbackground="#404040", foreground="#FFFFFF", font=("Segoe UI", 15))

        self.frame = ttk.Frame(master)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Center the frame in the window
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Center the frame in the window
        self.frame.grid(row=0, column=0, padx=80, pady=20, sticky="nsew")

        # Padding values
        padx_value = 30
        pady_value = 10

        # Set reference string at top
        self.reference_string_label = ttk.Label(self.frame, text="Reference String:")
        self.reference_string_label.grid(row=0, column=0, pady=pady_value, padx=padx_value, sticky="e")

        # Increase the width of the reference string entry
        self.reference_string_entry = ttk.Entry(self.frame, width=30)
        self.reference_string_entry.grid(row=0, column=1, pady=pady_value, padx=padx_value, sticky="w")

        self.page_frames_label = ttk.Label(self.frame, text="Page Frames:")
        self.page_frames_label.grid(row=1, column=0, pady=pady_value, padx=padx_value, sticky="e")

        # Increase the width of the page frames entry
        self.page_frames_entry = ttk.Entry(self.frame, width=30)
        self.page_frames_entry.grid(row=1, column=1, pady=pady_value, padx=padx_value, sticky="w")

        self.algorithm_label = ttk.Label(self.frame, text="Algorithm:")
        self.algorithm_label.grid(row=2, column=0, pady=pady_value, padx=padx_value, sticky="e")

        self.algorithms = ["LRU", "FIFO", "Optimal"]
        self.algorithm_combobox = ttk.Combobox(self.frame, values=self.algorithms)
        self.algorithm_combobox.grid(row=2, column=1, pady=pady_value, padx=padx_value, sticky="w")
        self.algorithm_combobox.set("LRU")

        # Create the "Simulate" button with the new style and decreased width
        self.simulate_button = ttk.Button(self.frame, text="Simulate", command=self.simulate, style="TRoundedButton.TButton", width=10)
        self.simulate_button.grid(row=3, column=0, columnspan=2, pady=20, sticky="nsew")

        self.result_label = ttk.Label(self.frame, text="")
        self.result_label.grid(row=4, column=0, columnspan=1, pady=pady_value, sticky="nsew")

        # Create the "Exit" button with the new style and decreased width
        self.exit_button = ttk.Button(self.frame, text="Exit", command=self.master.destroy, style="TRoundedButton.TButton", width=10)
        self.exit_button.grid(row=5, column=0, columnspan=2, pady=20, sticky="nsew")

    def simulate(self):
        reference_string = self.reference_string_entry.get().split()
        page_frames = int(self.page_frames_entry.get())

        if not reference_string or not self.is_valid_reference_string(reference_string):
            self.result_label.config(text="Invalid reference string. Please enter a valid space-separated string.")
            return

        algorithm = self.algorithm_combobox.get()

        reference_string = list(map(int, reference_string))

        if algorithm == "LRU":
            page_faults = self.lru_page_replacement(page_frames, reference_string)
        elif algorithm == "FIFO":
            page_faults = self.fifo_page_replacement(page_frames, reference_string)
        elif algorithm == "Optimal":
            page_faults = self.optimal_page_replacement(page_frames, reference_string)
        else:
            self.result_label.config(text="Invalid algorithm selected.")
            return

        result_text = f"{algorithm} Page Faults: {page_faults}"
        self.result_label.config(text=result_text)

    def lru_page_replacement(self, page_frames, reference_string):
        page_frames_order = deque(maxlen=page_frames)
        page_faults = 0

        for page in reference_string:
            if page not in page_frames_order:
                page_faults += 1
            else:
                page_frames_order.remove(page)

            page_frames_order.append(page)

        return page_faults

    def fifo_page_replacement(self, page_frames, reference_string):
        page_frames_queue = deque(maxlen=page_frames)
        page_faults = 0

        for page in reference_string:
            if page not in page_frames_queue:
                page_frames_queue.append(page)
                page_faults += 1

        return page_faults

    def optimal_page_replacement(self, page_frames, reference_string):
        page_frames_order = deque(maxlen=page_frames)
        page_faults = 0

        for index, page in enumerate(reference_string):
            if page not in page_frames_order:
                if len(page_frames_order) == page_frames:
                    page_to_remove = self.find_optimal_page_to_remove(reference_string[index + 1:], page_frames_order)
                    page_frames_order.remove(page_to_remove)
                page_frames_order.append(page)
                page_faults += 1

        return page_faults

    def find_optimal_page_to_remove(self, future_reference, current_page_frames):
        for page in current_page_frames:
            if page not in future_reference:
                return page
        return current_page_frames[0]

    def is_valid_reference_string(self, reference_string):
        try:
            list(map(int, reference_string))
            return True
        except ValueError:
            return False

def main():
    root = tk.Tk()
    app = PageReplacementSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
