from os import environ
from subprocess import call

num_files = 5

for file_number in range(num_files):
    environ['file_number'] = '%s'%file_number

    call(['runipy','TestData.ipynb'])
