import psutil

# cpu usage
print(type(psutil.cpu_percent(interval=1)))
print(type(psutil.cpu_percent(interval=1)), ": ", psutil.cpu_percent(interval=1))

# hard disk usage
print(type(str(psutil.disk_usage('/'))), ": ", psutil.disk_usage('/'))

print(type(psutil.virtual_memory()), ": ", psutil.virtual_memory())

