import pandas as pd
import datetime as dt

# Використання теперішнього часу для створення словника, який буде використано для створення DataFrame
now = dt.datetime.now()
data = {
    "year": [now.year],
    "month": [now.month],
    "day": [now.day],
    "hour": [now.hour],
    "minute": [now.minute],
    "second": [now.second]
}

# Створення DataFrame зі словника
data_frame = pd.DataFrame(data)

# Виведення DataFrame
print(data_frame)

# Збереження DataFrame у файл CSV без індексу
data_frame.to_csv("filename.csv", index=False)
