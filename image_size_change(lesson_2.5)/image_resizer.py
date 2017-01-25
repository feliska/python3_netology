import os.path
import subprocess
import glob
from multiprocessing import Pool


source = 'Source'
result = 'Result'

images = glob.glob(os.path.join(source, "*.jpg"))


def resize_img(filename):
    subprocess.run(['sips', '--resampleWidth', '200', filename])

# Создание папки "Result", если она не существует
try:
    os.mkdir(result)
except FileExistsError:
    print("Папка 'Result' уже существует")

for f in images:
    subprocess.run(['cp', f, result])

ready_img = glob.glob(os.path.join(result, "*.jpg"))
# parallel processing
pool = Pool(processes=4)
pool.map(resize_img, ready_img)
pool.close()
pool.join()
