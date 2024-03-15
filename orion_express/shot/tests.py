from django.test import TestCase
from TimeWithFrames import TimeWithFrames
# Create your tests here.
# Создаем два объекта TimeWithFrames
time1 = TimeWithFrames("01:00:13:00")
time2 = TimeWithFrames("01:00:05:00")

# Вычитаем время time2 из time1
time1.subtract_time(time2)

# Выводим результат
print(time1)  # Результат: 00:00:08:00
