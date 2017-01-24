import os.path
import subprocess
import glob

source = 'Source'
result = 'Result'

images = glob.glob(os.path.join(source, "*.jpg"))

# Создание папки "Result", если она не существует
try:
    os.mkdir(result)
except FileExistsError:
    print("Папка 'Result' уже существует")

for f in images:
    subprocess.run(['cp', f, result])

ready_img = glob.glob(os.path.join(result, "*.jpg"))

for img in ready_img:
    subprocess.run(['sips', '--resampleWidth', '200', img])
