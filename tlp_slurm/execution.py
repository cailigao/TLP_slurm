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
    Make the file executable
    :param path:
    :return:
    """
    subprocess.run(['chmod', '755', path])


def run_cmd(dir, cmd):
    """
    Executes the command in the specified directory
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
    Find execution file
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

    :param script:
    :param threads:
    :param jobid_list:
    :return:
    """
    if config.is_windows:
        # Run locally
        for jobid in jobid_list:
            out_file = script.parent / f'{script.stem}-{jobid}.out'
            cmd = f'{script} {jobid} > {out_file} 2>&1'
            run_cmd(Path.cwd(), cmd)
    else:
        if get_global('use_slurm') == '0':
            # Run locally
            for jobid in jobid_list:
                out_file = script.parent / f'{script.stem}-{jobid}.out'
                cmd = f'{script} {jobid} > {out_file} 2>&1'
                run_cmd(Path.cwd(), cmd)
        else:
            # Run in slurm
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
