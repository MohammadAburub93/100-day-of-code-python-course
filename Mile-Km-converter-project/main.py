from tkinter import *


def mile_km_converter():
    miles_value = int(entry_value.get())
    km_result = round(miles_value * 1.609)
    result_label.config(text=f"{km_result}")


window = Tk()
window.title("Mile to Km converter")
window.minsize(width=200, height=100)
window.config(padx=50, pady=20)

entry_value = Entry(width=10)
entry_value.grid(column=1, row=0)

miles_label = Label(text="Mile")
miles_label.grid(column=2, row=0)

km_label = Label(text="Km")
km_label.grid(column=2, row=1)

equal_to_label = Label(text="is equal to")
equal_to_label.grid(column=0, row=1)

result_label = Label(text="0")
result_label.grid(column=1, row=1)

calculate_button = Button(text="calculate", command=mile_km_converter)
calculate_button.grid(column=1, row=2)




















window.mainloop()
