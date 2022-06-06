#!/usr/bin/python
# -*- coding:utf-8 -*-
from .execution import find_executable, run_cmd
from .global_var import set_global, get_global
import sys
from pathlib import Path


def detect_slurm():
    sinfo = find_executable('sinfo')
    if sinfo is None:
        set_global('use_slurm', '0')
        return
    if get_global('use_slurm') == '0':
        sys.stderr.write('--\n')
        sys.stderr.write(f"-- Detected Slurm with 'sinfo' binary in {sinfo}.\n")
        sys.stderr.write('--          Slurm disabled by use_slurm=false\n')
        return
    set_global('use_slurm', '1')

    # sinfo信息
    output = run_cmd(Path.cwd(),
                     "sinfo --exact -o '%N %D %c %m %t %P' | grep \* | grep -v alloc | grep -v drained | grep -v interactive")
    if output is None:
        return
    host = {}
    lines = output.split('\n')
    for line in lines:
        strs = line.split(' ')
        cpus = int(strs[2])
        mem = int(strs[3]) // 1024
        nodes = int(strs[1])

        if f'{cpus}-{mem}' in host.keys():
            host[f'{cpus}-{mem}'] += nodes
        else:
            host[f'{cpus}-{mem}'] = nodes
    print(f'host: {host}')
    set_global('slurm_info', host)


def get_slurm_min_cpus():
    host = get_global('slurm_info')
    if host is None:
        return None
    cpus, mem = sorted(host.keys())[0].split('-')
    return cpus
