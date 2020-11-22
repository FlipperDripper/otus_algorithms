import time
from os import listdir
import os, fnmatch
import multiprocessing
from multiprocessing.managers import BaseManager
from prettytable import PrettyTable
import re

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


class BaseTest:

    def __init__(self, path, input_transform=None, output_transform=None, test_files_prefix='test'):
        self.output_transform = output_transform
        self.input_transform = input_transform
        self.path = path
        self.test_files_prefix = test_files_prefix
        self.test_source = TestSource(path, test_files_prefix)

    def prepared_data(self, input_data, output_data):
        prepared_input = input_data
        prepared_output = output_data
        if self.input_transform:
            prepared_input = self.input_transform(input_data)
        if self.output_transform:
            prepared_output = self.output_transform(output_data)
        return prepared_input, prepared_output

    def beautify_output(self, got, expected, test_name, time):
        if got == expected:
            print(Result(f'{test_name} passed in {time}ms', 'success'))
            print(f'got: {got}, expected: {expected}')
        else:
            print(Result(f'{test_name} failed in {time}ms', 'error'))
            print(f'got: {got}, expected: {expected}')

    def timeout_output(self, test_name, time):
        return Result(f'{test_name} failed in {time}s', 'error')


class Test(BaseTest):

    def __init__(self, test_function, path, input_transform=None, output_transform=None, test_files_prefix='test'):
        super(Test, self).__init__(path, input_transform, output_transform, test_files_prefix)
        self.test_function = test_function

    def run_case(self, test_name, input_data, output_data):
        prepared_input, prepared_output = self.prepared_data(input_data, output_data)

        def limited_func():
            t = time.process_time()
            result = self.test_function(prepared_input)
            elapsed_time = time.process_time() - t
            self.beautify_output(result, prepared_output, test_name, elapsed_time)

        assert_timeout(5, limited_func, self.timeout_output(test_name, 5)).join()

    def start(self):
        i = 0
        for case in self.test_source.source():
            self.run_case(f'{self.test_files_prefix} {i}', case['input'], case['output'])
            i += 1


class ComparableTest(BaseTest):
    def __init__(self, test_functions, path, input_transform=None, output_transform=None, test_files_prefix='test',
                 timeout=5):
        super(ComparableTest, self).__init__(path, input_transform, output_transform, test_files_prefix)
        self.timeout = timeout
        self.test_functions = test_functions
        BaseManager.register('ComparableData', ComparableData)
        manager = BaseManager()
        manager.start()
        self.compare_data: ComparableData = manager.ComparableData()

    def recursion_error(self):
        print(f'{CREDBG}RECURSION ERROR{ENDC}')

    def run_case(self, test_name, input_data, output_data):
        prepared_input, prepared_output = self.prepared_data(input_data, output_data)

        def limited_func(compare_data: ComparableData, func, func_name):
            compare_data.set(test_name, func_name)
            t = time.process_time()
            result = None
            try:
                result = func(prepared_input)
            except RecursionError:
                self.recursion_error()
            elapsed_time = time.process_time() - t
            is_truth = result == prepared_output
            compare_data.set(test_name, func_name, result, prepared_output, elapsed_time, is_truth)
            self.beautify_output(result, prepared_output, f'{test_name} {func_name}', elapsed_time)

        for func_name in self.test_functions:
            assert_timeout(5, limited_func, self.timeout_output(f'{test_name} {func_name}', self.timeout),
                           (self.compare_data, self.test_functions[func_name], func_name)).join()

    def start(self):
        i = 0
        for case in self.test_source.source():
            self.run_case(f'{self.test_files_prefix} {i}', case['input'], case['output'])
            i += 1
        result_table = self.compare_data.get()
        self.print_compare_table(result_table)

    def print_compare_table(self, table_data):
        table = PrettyTable()
        field_names = ['Test']
        rows = []
        i = 0
        for test_name in table_data:
            rows.append([])
            rows[i].append(test_name)
            for func_name in table_data[test_name]:
                if func_name not in field_names:
                    field_names.append(func_name)
                data = table_data[test_name][func_name]
                if data['status']:
                    rows[i].append(f'{CGREENBG}success{ENDC} in {data["elapsed_time"]}')
                else:
                    if data['elapsed_time'].is_known():
                        rows[i].append(f'{CREDBG}error{ENDC} in {data["elapsed_time"]}')
                    else:
                        rows[i].append(f'{CREDBG}Time out in {self.timeout}s{ENDC}')
            if len(rows[i]) < len(field_names):
                for j in range(len(field_names) - len(rows[i])):
                    rows[i].append(f'{CREDBG}Time out{ENDC}')
            i += 1
        table.field_names = field_names
        table.add_rows(rows)
        table.align = 'l'
        print(table)


def assert_timeout(time_sec, func, timeout_message, args=tuple()):
    p = multiprocessing.Process(target=func, args=args)
    p.start()
    p.join(time_sec)
    if p.is_alive():
        print(timeout_message)
        p.terminate()
        p.join()
    return p


class TimeMs:
    def __init__(self, seconds):
        self.seconds = seconds

    def __str__(self):
        if self.seconds is None:
            return ''
        ms = round(self.seconds * 1000, 4)
        return f'{ms} ms'

    def is_known(self):
        return bool(self.seconds)


class TestSource:
    def __init__(self, path, prefix):
        self.prefix = prefix
        self.path = path
        self.input_files = []
        self.output_files = []
        self.grab_file_names()

    def join_files(self, file_names):
        res = list(map(lambda fn: os.path.join(self.path, fn), file_names))
        res.sort(key=lambda filename: int(re.match(r".*\.(\d+)\.(in|out)", filename).group(1)))
        return res

    def grab_file_names(self):
        all_files = listdir(self.path)
        test_source = list(filter(lambda filename: fnmatch.fnmatch(filename, f'{self.prefix}*'), all_files))
        self.input_files = self.join_files(
            list(filter(lambda filename: fnmatch.fnmatch(filename, '*.in'), test_source)))
        self.output_files = self.join_files(
            list(filter(lambda filename: fnmatch.fnmatch(filename, '*.out'), test_source)))
        print(self.input_files, self.output_files)

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


class ComparableData:
    def __init__(self):
        self.data = {}

    def set(self, test_name, func_name, result=None, expected=None, elapsed_time=None, status=None):
        if test_name not in self.data:
            self.data[test_name] = {}
        self.data[test_name][func_name] = {
            'func_name': func_name,
            'result': result,
            'expected': expected,
            'elapsed_time': TimeMs(elapsed_time),
            'status': status
        }

    def get(self):
        return self.data
