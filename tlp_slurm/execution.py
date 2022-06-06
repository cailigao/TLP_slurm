#!/usr/bin/python
# -*- coding:utf-8 -*-
import subprocess
import os
from .global_var import get_global
from pathlib import Path
from tlp_slurm import config
from simple_slurm import Slurm


def make_executable(path):
    """
    将文件设为可执行文件
    :param path:
    :return:
    """
    subprocess.run(['chmod', '755', path])


def run_cmd(dir, cmd):
    """
    在指定的目录下执行命令
    :param dir:
    :param cmd:
    :return:
    """
    cwd = Path.cwd()
    os.chdir(dir)
    status, output = subprocess.getstatusoutput(cmd)
    os.chdir(cwd)
    if status == 0:
        return output
    return None


def find_executable(exec):
    """
    查找执行文件
    which指令会在环境变量$PATH设置的目录里查找符合条件的文件。
    """
    if config.is_windows:
        status, path = subprocess.getstatusoutput(f'where {exec}')
    else:
        status, path = subprocess.getstatusoutput(f'which {exec} 2> /dev/null')
    if status == 0:
        return path
    return None


def get_jobid_shell_code():
    string = ''
    if config.is_windows:
        string += 'set id=%1\n'
    else:
        if get_global('use_slurm') == '0':
            string += 'id=$1\n'
        else:
            string += 'id=$SLURM_ARRAY_TASK_ID\n'
    return string


def submit_job(script, threads, jobid_list, dependency_jobid=[]):
    """
    提交作业
    :param script:
    :param threads:
    :param jobid_list:
    :return:
    """
    if config.is_windows:
        # 在本地运行
        for jobid in jobid_list:
            out_file = script.parent / f'{script.stem}-{jobid}.out'
            cmd = f'{script} {jobid} > {out_file} 2>&1'
            run_cmd(Path.cwd(), cmd)
    else:
        if get_global('use_slurm') == '0':
            # 在本地运行
            for jobid in jobid_list:
                out_file = script.parent / f'{script.stem}-{jobid}.out'
                cmd = f'{script} {jobid} > {out_file} 2>&1'
                run_cmd(Path.cwd(), cmd)
        else:
            # 在slurm中运行
            out_file = script.parent / f'{script.stem}_{Slurm.JOB_ARRAY_MASTER_ID}_{Slurm.JOB_ARRAY_ID}.out'
            dependency = {}
            for jobid in dependency_jobid:
                dependency['after'] = jobid

            slurm = Slurm(
                array=jobid_list,
                cpus_per_task=threads,
                job_name=script.stem,
                output=out_file,
            )
            if len(dependency) > 0:
                slurm.set_dependency(dependency)
            print(slurm)
            return slurm.sbatch(str(script))


if __name__ == '__main__':
    pass
