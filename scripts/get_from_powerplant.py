"""
Downloads files from powerplant in the /workspace/cfphxd/Kaka/data/ directory.
Saves the files to a local data directory, where the sub directory structure matches that
of the directories where the data was obtained on powerplant
"""

from urllib import request
from urllib.error import HTTPError
import re
import os
from platform import platform


def get_files(path):
    if path[-1] is not '/':
        path += '/'  # so that url building works

    slash = '\\' if 'Windows' in platform() else '/'
    powerplant_address = 'http://storage.powerplant.pfr.co.nz/workspace/cfphxd/Kaka/data/'

    # Reads the pages HTML
    urlpath = request.urlopen(powerplant_address + path)
    page_html = urlpath.read().decode('utf-8')

    # Checks that the local data directory has sub directories that match powerplant
    cwd = os.getcwd()
    cwdsplit = cwd.split(slash)
    rebuild = []
    for dir in cwdsplit:  # backtracks to Kaka dir to go to the data dir
        rebuild.append(dir)
        if dir == 'Kaka':
            break
    rebuild.append('data')
    rebuild.append(path.replace('/', slash))
    savepath = slash.join(rebuild)
    # Creates the subdirectories for the files if they don't exist
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    # searches for the links to files, retrieves the files and saves them
    # to the directory that matches their directory on powerplant
    pattern = re.compile('(?<=href=")((\S+)((\.gz)|(\.csv)))(?=">)')
    for match in pattern.finditer(page_html):
        address = powerplant_address + path + match.group(1)
        save = savepath + match.group(1)
        try:
            request.urlretrieve(address, save)
        except HTTPError as e:
            print("Could not retrieve: " + address + ": " + e.msg)


def run():
    get_files('genotype/Ach')
    get_files('genotype/East12')
    get_files('genotype/GBS_Workshop_Maize')
