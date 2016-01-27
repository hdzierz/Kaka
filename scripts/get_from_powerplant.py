from urllib import request
from urllib.error import HTTPError
import re
import os
from platform import platform


def get_files(path):
    if path[-1] is not '/':
        path = path + '/'
    # print('Path: ' + path)

    slash = '\\' if 'Windows' in platform() else '/'
    powerplant_address = 'http://storage.powerplant.pfr.co.nz/workspace/cfphxd/Kaka/data/'
    urlpath = request.urlopen(powerplant_address + path)
    string = urlpath.read().decode('utf-8')
    pattern = re.compile('(?<=href=")((\S+)((\.gz)|(\.csv)))(?=">)')
    cwd = os.getcwd()
    # print("Current working directory: " + cwd)
    cwdsplit = cwd.split(slash)
    # print("CWD split: " + str(cwdsplit))
    rebuild = []
    for dir in cwdsplit:
        rebuild.append(dir)
        if dir == 'Kaka':
            break
    rebuild.append('data')
    rebuild.append(path.replace('/', slash))
    savepath = slash.join(rebuild)
    # print("Save Path: " + savepath)
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    for match in pattern.finditer(string):
        address = powerplant_address + path + match.group(1)
        # print("Address: " + address)
        save = savepath + match.group(1)
        # print("Save: " + save)
        try:
            request.urlretrieve(address, save)
        except HTTPError as e:
            print("Could not retrieve: " + address + ": " + e.msg)


def run():
    get_files('genotype/Ach')
    get_files('genotype/East12')
    get_files('genotype/GBS_Workshop_Maize')
