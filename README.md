# DirTreeCloner
This script can clone a complete tree structure from a root folder into another one, replacing files with placeholders or a file list txt (with file properties)

Works best on Linux, in Windows it works but is much slower.

TO FIX:

Traceback (most recent call last):
  File ".\DirTreeCloner.py", line 100, in <module>
    generateFileList(dest_path, dirpath, filenames, stats=stats)
  File ".\DirTreeCloner.py", line 62, in generateFileList
    file_list.write(line+'\n')
  File "C:\Program Files\Python38\lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
UnicodeEncodeError: 'charmap' codec can't encode character '\uff08' in position 16: character maps to <undefined>
