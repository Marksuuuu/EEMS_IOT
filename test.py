import tkinter as tk
from tkinter import Label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
from PIL import Image, ImageTk

def create_donut_chart():
    # Donut chart data
    labels = ['A', 'B', 'C', 'D']
    sizes = [30, 40, 20, 10]
    colors = ['red', 'green', 'blue', 'orange']

    # Create a figure and a subplot for the donut chart
    fig, ax = plt.subplots()
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Create the donut chart
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        wedgeprops={'width': 0.4},  # Set the width to create a donut chart
    )

    # Customize the labels
    for text, autotext in zip(texts, autotexts):
        text.set(size=12, weight='bold')
        autotext.set(size=12, weight='bold')

    # Save the chart as an image in memory
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    chart_image = Image.open(image_stream)

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Donut Chart in Label Example")

    # Convert the Matplotlib chart image to a Tkinter PhotoImage
    tk_chart_image = ImageTk.PhotoImage(chart_image)

    # Create a label and display the chart image
    label = Label(root, image=tk_chart_image)
    label.pack()

    # Start the Tkinter main loop
    root.mainloop()

# Call the function to create a window with the donut chart in a label
create_donut_chart()
