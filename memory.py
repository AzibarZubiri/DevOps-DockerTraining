import psutil
cpu = psutil.cpu_percent()
memory = psutil.virtual_memory().percent
print(f"CPU: {cpu}%")
print(f"Memory: {memory}%")
