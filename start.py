#!/usr/bin/python
# -*- coding:utf-8 -*-
import argparse
from pathlib import Path
from tlp_slurm.execution import run_cmd, make_executable, get_jobid_shell_code, submit_job
from tlp_slurm import config
from tlp_slurm.detect_slurm import detect_slurm
from tlp_slurm.global_var import set_default
import json


class Start:
    def __init__(self, argsFile):
        args = json.load(argsFile.open())
        # ------------------------解析参数-------------------------
        # 数据分割执行程序参数设置
        split = args.get('split')
        self.split_bin = Path(split.get('bin')).resolve()

        split_type = split.get('type', 'c')
        self.split_exe = ''
        if split_type.lower() == 'python':
            self.split_exe = 'python'
        elif split_type.lower() == 'java':
            self.split_exe = 'java'
        elif split_type.lower() == 'c':
            self.split_exe = ''

        split_input = split.get('input')
        self.split_input_my_input = split_input.get('my_input')
        self.split_input_value = Path(split_input.get('value')).resolve()

        split_output = split.get('output')
        self.split_output_my_output = split_output.get('my_output')
        self.split_output_value = Path(split_output.get('value')).resolve()

        self.split_my_args = split.get('my_args', '')

        # 主程序参数设置
        main = args.get('main')
        self.main_bin = Path(main.get('bin')).resolve()

        main_type = main.get('type', 'c')
        self.main_exe = ''
        if main_type.lower() == 'python':
            self.main_exe = 'python'
        elif main_type.lower() == 'java':
            self.main_exe = 'java'
        elif main_type.lower() == 'c':
            self.main_exe = ''

        main_input = main.get('input')
        self.main_input_my_input = main_input.get('my_input')

        main_output = main.get('output')
        self.main_output_my_output = main_output.get('my_output')
        self.main_output_value = Path(main_output.get('value')).resolve()

        main_threads = main.get('threads', {})
        self.main_threads_my_threads = main_threads.get('my_threads', '')
        self.main_threads_value = main_threads.get('value', 1)

        self.main_my_args = main.get('my_args', '')

    def start(self):
        # 分割数据
        data_path = self.split_output_value / config.DATA_DIR
        cmd = f'{self.split_exe} {self.split_bin} {self.split_input_my_input} {self.split_input_value} {self.split_output_my_output} {data_path} {self.split_my_args}'

        run_cmd(Path.cwd(), cmd)

        # 分割后的文件作为每个作业的数据
        data_dict = {}
        job_id = 1
        for path in data_path.iterdir():
            if path.is_file():
                data_dict[job_id] = path
                job_id += 1
        jobid_list = range(1, job_id)

        # 生成主程序的脚本文件
        script_path = self.split_output_value / config.SCRIPT_DIR
        script_path.mkdir(parents=True, exist_ok=True)
        if config.is_windows:
            script_file = script_path / f'main.bat'
            with script_file.open('w') as f:
                f.write(get_jobid_shell_code())

                for job_id, path in data_dict.items():
                    f.write(f'if %id%=={job_id} ( \n')
                    f.write(f'  set input={path} \n')
                    f.write(') \n')
                    f.write('\n')

                f.write('\n')
                f.write(f'{self.main_exe} {self.main_bin} ^\n')
                f.write(f'  {self.main_input_my_input} %input% ^\n')
                f.write(f'  {self.main_output_my_output} {self.main_output_value} ^\n')
                if self.main_threads_my_threads.strip():
                    f.write(f'  {self.main_threads_my_threads} {self.main_threads_value} ^\n')
                f.write(f'  {self.main_my_args} ^\n')
        else:
            script_file = script_path / f'main.sh'
            with script_file.open('w') as f:
                f.write('#!/bin/sh \n')
                f.write('\n')
                f.write('\n')
                f.write(get_jobid_shell_code())
                f.write('\n')

                for job_id, path in data_dict.items():
                    f.write(f'if [ $id -eq {job_id} ] ; then \n')
                    f.write(f'  input={path} \n')
                    f.write('fi \n')
                    f.write('\n')

                f.write('\n')
                f.write(f'{self.main_exe} {self.main_bin} \\\n')
                f.write(f'  {self.main_input_my_input} $input \\\n')
                f.write(f'  {self.main_output_my_output} {self.main_output_value} \\\n')
                if self.main_threads_my_threads.strip():
                    f.write(f'  {self.main_threads_my_threads} {self.main_threads_value} \\\n')
                f.write(f'  {self.main_my_args} \\\n')
            make_executable(script_file)

        # 提交作业
        submit_job(script_file, self.main_threads_value, jobid_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--argsFile', type=str, required=True, help='arguments json file')
    args = parser.parse_args()
    args.argsFile = Path(args.argsFile).resolve()

    set_default()
    detect_slurm()
    start = Start(args.argsFile)
    start.start()
