import tkinter as tk
from tkinter import ttk
import openai
import requests
from requests.structures import CaseInsensitiveDict
import json
from PIL import Image

openai.api_key = ("")
model = "image-alpha-001"
resolutions = ["512x512", "1024x1024", "2048x2048"]

class App:
    def __init__(self, master):
        self.master = master
        master.title("OpenAI Image Generator")

        self.prompt_label = tk.Label(master, text="Prompt:",bg="#EEEEEE", anchor="w", font=("Helvetica", 10, "bold"))
        self.prompt_label.grid(row=0, column=0, sticky="w", padx=3)

        self.prompt_text = tk.Text(master, height=2)
        self.prompt_text.grid(row=0, column=1, columnspan=2, sticky="w", padx=3)

        self.num_label = tk.Label(master, text="Number of Images:", anchor="w", bg="#EEEEEE", font=("Helvetica", 10, "bold"))
        self.num_label.grid(row=1, column=0, sticky="we", padx=3)

        self.num_entry = tk.Entry(master)
        self.num_entry.grid(row=1, column=1, sticky="we", padx=3)

        self.res_label = tk.Label(master, text="Select Resolution:", anchor="w", bg="#EEEEEE", font=("Helvetica", 10, "bold"))
        self.res_label.grid(row=2, column=0, sticky="w", padx=3)

        self.res_choice = tk.StringVar()
        self.res_choice.set(resolutions[0])
        self.res_dropdown = tk.OptionMenu(master, self.res_choice, *resolutions)
        self.res_dropdown.grid(row=2, column=1, sticky="W", padx=3)

        self.generate_button = tk.Button(master, text="Generate Images", command=self.generate_images, bg="#C4C4C4", font=("Helvetica", 12, "bold"))
        self.generate_button.grid(row=3, columnspan=3, sticky="we", padx=3, pady=3)

        self.status_label = tk.Label(master, text="", anchor="e", font=("Helvetica", 10, "bold"))
        self.status_label.grid(row=2, column=2, sticky="e", padx=3)

        # Make widgets scale with window size
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_rowconfigure(3, weight=1)

    def generate_images(self):
        prompt = self.prompt_text.get("1.0", "end-1c")
        num_of_images = int(self.num_entry.get())
        resolution = self.res_choice.get()

        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {openai.api_key}"

        num_images = num_of_images
        status_text = ""  # initialize status text

        for i in range(num_images):
            data = """
            {{
                "model": "{}",
                "prompt": "{}",
                "num_images":1,
                "size":"{}",
                "response_format":"url"
            }}
            """.format(model, prompt, resolution)

            resp = requests.post("https://api.openai.com/v1/images/generations", headers=headers, data=data)

            if resp.status_code != 200:
                raise ValueError("Failed to generate image")

            response_text = resp.text
            response_json = json.loads(response_text)

            image_url = response_json["data"][0]["url"]
            image_response = requests.get(image_url)

            with open(f"image_{i+1}.jpg", "wb") as f:
                f.write(image_response.content)

            self.status_label.config(text=f"Image {i+1} generated and saved")
            self.master.update()  # Force the window to update

        self.status_label.config(text="All images generated and saved")
        self.master.update()  # Force the window to update

        

root = tk.Tk()
root.configure(background='#EEEEEE')
app = App(root)
root.mainloop()
