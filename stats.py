import os
import psutil


print('Memory usage: ', psutil.virtual_memory())
print('CPU usage: ', psutil.cpu_percent(), '%')


