import time
from os import listdir
from os.path import isfile
import os, fnmatch

CREDBG = '\33[41m'
CGREENBG = '\33[42m'
CWHITE = '\33[30m'
ENDC = '\033[0m'


class Result:
    def __init__(self, message, status):
        self.message = message
        self.status = status

    def __str__(self):
        bg_color = ''
        if self.status == 'success':
            bg_color = CGREENBG
        if self.status == 'error':
            bg_color = CREDBG
        return f'''
{bg_color}{self.status.upper()}{ENDC}
{self.message}
'''


class Test:

    def __init__(self, test_function, path, input_transform=None, output_transform=None, test_files_prefix='test'):
        self.output_transform = output_transform
        self.input_transform = input_transform
        self.path = path
        self.test_function = test_function
        self.test_files_prefix = test_files_prefix
        self.test_source = TestSource(path, test_files_prefix)

    def run_case(self, test_name, input_data, output_data):
        t = time.process_time()
        prepared_input = input_data
        prepared_output = output_data
        if self.input_transform:
            prepared_input = self.input_transform(input_data)
        if self.output_transform:
            prepared_output = self.output_transform(output_data)
        result = self.test_function(prepared_input)
        elapsed_time = time.process_time() - t
        if prepared_output == result:
            print(Result(f'{test_name} passed in {elapsed_time}ms', 'success'))
            print(f'got: {result}, expected: {output_data}')
        else:
            print(Result(f'{test_name} failed in {elapsed_time}ms', 'error'))
            print(f'got: {result}, expected: {output_data}')

    def start(self):
        i = 0
        for case in self.test_source.source():
            self.run_case(f'{self.test_files_prefix} {i}', case['input'], case['output'])
            i += 1


class TestSource:
    def __init__(self, path, prefix):
        self.prefix = prefix
        self.path = path
        self.input_files = []
        self.output_files = []
        self.grab_file_names()

    def join_files(self, file_names):
        res = list(map(lambda fn: os.path.join(self.path, fn), file_names))
        res.sort()
        return res

    def grab_file_names(self):
        all_files = listdir(self.path)
        test_source = list(filter(lambda filename: fnmatch.fnmatch(filename, f'{self.prefix}*'), all_files))
        self.input_files = self.join_files(
            list(filter(lambda filename: fnmatch.fnmatch(filename, '*.in'), test_source)))
        self.output_files = self.join_files(
            list(filter(lambda filename: fnmatch.fnmatch(filename, '*.out'), test_source)))

    def source(self):
        i = 0
        while i < len(self.input_files) and i < len(self.output_files):
            yield {
                'input': open(self.input_files[i], 'r').read().rstrip(),
                'output': open(self.output_files[i], 'r').read().rstrip()
            }
            i += 1

    def __iter__(self):
        return self
