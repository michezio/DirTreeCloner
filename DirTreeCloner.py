'''
DirTreeCloner
Michele Abruzzese (@michezio)
2022-01-13

Usage:

python DirTreeCloner.py /source/folder /destination/folder [options]

[options]
--placeholders: generate placeholders for every file instead of a file list
--stats: add stats for each file as a string in file list (or as the content of the placeholder)
--silent: don't show any output
'''

import sys
import os
import time


_file_types = dict(
    document = ['pdf', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'html', 'htm'],
    picture = ['jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'gif'],
    audio = ['mp3', 'wav', 'flac', 'aac'],
    video = ['mov', 'avi', 'mp4', 'm4v', 'mkv', 'flv', '3gp', 'dvx'],
    archive = ['zip', 'rar', '7z', 'tar', 'gzip', 'gz'],
    executable = ['exe', 'bat', 'cmd', 'sh'])

_file_types = {value: key for key in _file_types for value in _file_types[key]}


def getSizeWithMult(size):
    if size >= 2**40:
        return f"{round(size/2**40, 2)} TiB ({size} B)"
    if size >= 2**30:
        return f"{round(size/2**30, 2)} GiB ({size} B)"
    if size >= 2**20:
        return f"{round(size/2**20, 2)} MiB ({size} B)"
    if size >= 2**10:
        return f"{round(size/2**10, 2)} KiB ({size} B)"
    return f"{size} B"


def getFileStats(file_path):
    name = file_path.split(os.path.sep)[-1]
    try:
        stats = os.stat(file_path)
    except:
        return f"BAD NAMED FILE: {file_path}"
    size = getSizeWithMult(stats.st_size)
    try:
        c_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_ctime))
    except:
        c_time = "ERROR"
    try:
        m_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))
    except:
        m_time = "ERROR"
    extension = name.split('.')[-1].lower()
    type = 'other' if extension not in _file_types.keys() else _file_types[extension]
    return f"{name}  [{type} ({extension}); {size}; {m_time} (created {c_time})]"


def generateFileList(dest_path, orig_path, filenames, stats=True):
    if len(filenames) == 0:
        return
    with open(dest_path+"FileList.txt", "w", encoding="utf-8") as file_list:
        for file in filenames:
            path = orig_path + file
            line = getFileStats(path) if stats else file
            file_list.write(line+'\n')

def generatePlaceholders(dest_path, orig_path, filenames, extensions=True, stats=True):
    if len(filenames) == 0:
        return
    for file in filenames:
        path = orig_path + file
        line = getFileStats(path).split("[")[-1][:-1]
        with open(dest_path+file, "w", encoding="utf-8") as file_placeholder:
            if stats:
                file_placeholder.write(line+'\n')
            else:
                pass
        


if __name__ == '__main__':

    root = sys.argv[1]
    root_start = len(os.path.sep.join(root.split(os.path.sep)[:-1]))+1
    dest = sys.argv[2]
    placeholders = '--placeholders' in sys.argv[3:]
    stats = '--stats' in sys.argv[3:]
    silent = '--silent' in sys.argv[3:]

    ignore_folders = ["app data", "dati applicazioni", "program files", "programmi", "windows"]

    if dest[-1] != os.path.sep:
        dest += os.path.sep

    for (dirpath, dirnames, filenames) in os.walk(root):
        if any(substring in dirpath.lower() for substring in ignore_folders):
            print("IGNORED", dirpath)
            continue
        if dirpath[-1] != os.path.sep:
            dirpath += os.path.sep
        dest_path = dest+dirpath[root_start:]
        os.makedirs(dest_path)
        if not silent:
            print(dirpath)
        if placeholders:
            generatePlaceholders(dest_path, dirpath, filenames, stats=stats)
        else:
            generateFileList(dest_path, dirpath, filenames, stats=stats)