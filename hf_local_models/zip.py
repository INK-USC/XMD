import os
import zipfile
import shutil
# with zipfile.ZipFile('./bert-base-uncased-hatexplain.zip', 'r') as fp:
#     fp.extractall(path='tmp')

# print(os.listdir('./tmp'))

shutil.rmtree('tmp')


print(os.listdir())