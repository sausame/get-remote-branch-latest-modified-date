#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import subprocess
import sys
import time

from datetime import datetime

def tsToDatetime(ts):
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def getchar():
    sys.stdin.read(1)

def runCommand(cmd, shell=False):

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    output, unused_err = process.communicate()
    retcode = process.poll()

    if retcode is not 0:
        raise subprocess.CalledProcessError(retcode, cmd)

    if not isinstance(output, str):
        if isinstance(output, bytes):
            output = str(output, encoding = 'utf-8')

    return output

def run():

    cmd = 'git status'
    print(runCommand(cmd))

    print('*** Please check if there are some modifications')
    getchar()

    cmd = 'git branch --remote'
    output = runCommand(cmd)

    statuses = list()

    branches = output.split('\n')
    for branch in branches:

        branch = branch.strip()

        if len(branch) == 0 or '/HEAD ->' in branch:
            continue

        cmd = 'git checkout {}'.format(branch)
        runCommand(cmd)
        cmd = 'git log -1 --format=%at'
        ts = int(runCommand(cmd))

        statuses.append((ts, branch))

    statuses = sorted(statuses, key=lambda x: x[0], reverse=True)
    print('\n'.join(['{}:\t{}'.format(tsToDatetime(x), y) for x, y in statuses]))

if __name__ == '__main__':

    os.environ['TZ'] = 'Asia/Shanghai'
    time.tzset()

    run()
