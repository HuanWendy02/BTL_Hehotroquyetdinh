import tkinter as tk
from tkinter import messagebox
import joblib
from tkinter.font import Font
from PIL import Image, ImageTk
import geocoder
from datetime import datetime
import requests

classifier = joblib.load("dtm.joblib")

window = tk.Tk()
window.title("Weather")
window.geometry("1000x680")
window.configure(bg="#396285")
def real_format_response(weather):
    #print(weather)
    try:
        name = weather['name']
        description = weather['weather'][0]['description']
        temperature = weather['main']['temp']
        final_string = 'City: ' + str(name) + '\n'  + 'Description: ' + str(description) + '\n' + 'Temperature: ' + str(temperature) + ' °F'
    except:
        final_string = "Dữ liệu không chính xác"
    return final_string

def get_weather(city):
    weather_key = "4dc29810ecf0e9e9cdf1b447d87353a9"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
    response = requests.get(url, params=params)
    weather = response.json()

    label['text']= real_format_response(weather)

def predict_weather(event=None):
    temp_max = float(entry_temp_max.get())
    temp_min = float(entry_temp_min.get())
    wind = float(entry_wind.get())
    re_humidity = float(entry_re_humidity.get())

    if wind > 20:
        messagebox.showwarning(
            "Thông báo",
            "Trời : Gió mạnh \n Lưu ý: Cẩn trọng với lốc xoáy và gió giật",
        )
    elif re_humidity > 85:
        messagebox.showwarning(
            "Thông báo",
            "Độ ẩm vượt ngưỡng \n",
        )
    elif temp_max > 37:
        messagebox.showwarning(
            "Thông báo",
            "Nhiệt độ ở mức cao \n Lưu ý: Hạn chế ra đường vào thời điểm này! ",
        )
    elif temp_min < 10:
        messagebox.showwarning(
            "Thông báo",
            "Nhiệt độ thấp \n Lưu ý: Mặc ấm khi ra khỏi nhà",
        )
    else:
        prediction = classifier.predict([[temp_max,temp_min,wind,re_humidity]])
        label_result.configure(
            text="                    Dự báo thời tiết hôm nay:   " + prediction[0],
            font=("Helvetica", 20),
            justify="center",
        )

heading_font = Font(family="Helvetica", size=20, weight="bold")
label_title = tk.Label(
    window,
    text="HỆ THỐNG DỰ BÁO THỜI TIẾT VÀ ĐƯA RA CẢNH BÁO THIÊN TAI",
    font=heading_font,
    bg="#396285",
    fg="white",
)
label_title.pack(pady=(10, 20))

frame_inputs = tk.Frame(window, bg="#396285")
frame_inputs.pack(padx=50, pady=20, anchor="w")

label_font = Font(family="Time New Romans", size=14, weight="bold")

label_temp_max = tk.Label(
    frame_inputs, text="Nhiệt độ cao nhất", bg="#396285", fg="white", font=label_font
)
label_temp_max.grid(row=0, column=0, padx=10, sticky="w")
entry_temp_max = tk.Entry(frame_inputs)
entry_temp_max.grid(row=0, column=1)
label_unit_temp_max = tk.Label(
    frame_inputs, text="°C", bg="#396285", fg="white", font=label_font
)

label_unit_temp_max.grid(row=0, column=2)
entry_temp_max.bind("<Return>", lambda e: entry_temp_max.focus())

label_temp_min = tk.Label(
    frame_inputs, text="Nhiệt độ thấp nhất", bg="#396285", fg="white", font=label_font
)
label_temp_min.grid(row=1, column=0, padx=10, sticky="w")
entry_temp_min = tk.Entry(frame_inputs)
entry_temp_min.grid(row=1, column=1)
label_unit_temp_min = tk.Label(
    frame_inputs, text="°C", bg="#396285", fg="white", font=label_font
)
label_unit_temp_min.grid(row=1, column=2)
entry_temp_min.bind("<Return>", lambda e: entry_temp_min.focus())

label_wind = tk.Label(
    frame_inputs, text="Tốc độ gió", bg="#396285", fg="white", font=label_font
)
label_wind.grid(row=2, column=0, padx=10, sticky="w")
entry_wind = tk.Entry(frame_inputs)
entry_wind.grid(row=2, column=1)
label_unit_wind = tk.Label(
    frame_inputs, text="m/s", bg="#396285", fg="white", font=label_font
)
label_unit_wind.grid(row=2, column=2)
entry_wind.bind("<Return>", lambda e: entry_wind.focus())

label_re_humidity = tk.Label(
    frame_inputs, text="Độ ẩm", bg="#396285", fg="white", font=label_font
)
label_re_humidity.grid(row=3, column=0, padx=10, sticky="w")
entry_re_humidity = tk.Entry(frame_inputs)
entry_re_humidity.grid(row=3, column=1)
label_unit_re_humidity = tk.Label(
    frame_inputs, text="%", bg="#396285", fg="white", font=label_font
)
label_unit_re_humidity.grid(row=3, column=2)
entry_re_humidity.bind("<Return>", predict_weather)

predict_image = Image.open("predict.png")
predict_image = predict_image.resize((150, 50), Image.LANCZOS)
predict_photo = ImageTk.PhotoImage(predict_image)

button_predict = tk.Button(
    window,
    image=predict_photo,
    command=predict_weather,
    bd=0,
    bg="#396285",
    activebackground="#396285",
)
button_predict.pack(pady=(0, 20), anchor="w", padx=155)

label_result = tk.Label(
    window,
    text="",
    bg="#396285",
    fg="white",
    font=("Helvetica", 12, "bold"),
    justify="center",
)
label_result.pack(anchor="w")
frame_black = tk.Frame(window, bg="white", height=250)
frame_black.pack(fill="both", expand=True)
frame1 = tk.Frame(frame_black, bg="black", bd=1)    #80cffc
frame1.place(relwidth=0.75, relheight=0.10, relx=0.5, rely=0.10, anchor='n')

entry = tk.Entry(frame1, font=('Helvetica', 20))
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame1, font=('Helvetica', 18), text='Xem', fg="white", bg="blue", command=lambda: get_weather(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.30)

frame2 = tk.Frame(frame_black, bg="black", bd=5)
frame2.place(relwidth=0.75, relheight=0.70, relx=0.5, rely=0.20, anchor='n')

label = tk.Label(frame2, fg="blue", font=('Helvetica', 25), bg="black", text="Thời tiết hiện tại", anchor='nw', justify='left', border=30)
label.place(relwidth=1, relheight=1)
window.mainloop()

