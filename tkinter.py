import tkinter
from collections import deque

class PageReplacementSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Page Replacement Simulator")

        self.page_frames_label = tk.Label(master, text="Number of Page Frames:")
        self.page_frames_label.pack()

        self.page_frames_entry = tk.Entry(master)
        self.page_frames_entry.pack()

        self.reference_string_label = tk.Label(master, text="Reference String:")
        self.reference_string_label.pack()

        self.reference_string_entry = tk.Entry(master)
        self.reference_string_entry.pack()

        self.simulate_button = tk.Button(master, text="Simulate", command=self.simulate)
        self.simulate_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def simulate(self):
        page_frames = int(self.page_frames_entry.get())
        reference_string = self.reference_string_entry.get().split()

        if not reference_string or not self.is_valid_reference_string(reference_string):
            self.result_label.config(text="Invalid reference string. Please enter a valid space-separated string.")
            return

        page_frames = int(self.page_frames_entry.get())
        reference_string = list(map(int, reference_string))

        page_faults = self.fifo_page_replacement(page_frames, reference_string)
        self.result_label.config(text=f"Page Faults: {page_faults}")

    def fifo_page_replacement(self, page_frames, reference_string):
        page_frames_queue = deque(maxlen=page_frames)
        page_faults = 0

        for page in reference_string:
            if page not in page_frames_queue:
                page_frames_queue.append(page)
                page_faults += 1

        return page_faults

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
