
import sys
import os
from getopt import getopt, GetoptError
from .utils import move_files


DEFAULT_LOGFILE = "./group_mv.logs"
os.environ["LOGFILE"] = DEFAULT_LOGFILE

def main():
    group, source, dest, recursive, force = None, None, None, False, False
    try:
        opts, _ = getopt(sys.argv[1:], "hrfg:s:d:l:", "help recursive force group_name= source_dir= dest_dir= logfile=".split())
    except GetoptError:
        print("Usage: group_mv -g <group_name> -s <source_dir> -d <dest_dir>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in "-h --help".split():
            help_msg = f"""
            Moves files owned by users of a specified group from source to destination folder.

            Usage: group_mv -g <group_name> -s <source_dir> -d <dest_dir>

            Required parameters:
            -g, --group_name <GROUP NAME>
            -s, --source_dir <SOURCE FOLDER>
            -d, --dest_dir <DESTINATION FOLDER>

            Optional parameters:
            -r, --recursive \t\t move files of source folder and files in subdirectories
            -f, --force \t\t overwrite files in destination folder
            -l, --logfile <LOGFILE> \t use a custom logfile (default: {DEFAULT_LOGFILE})
            """
            print(help_msg)
            sys.exit()
        elif opt in "-r --recursive".split():
            recursive = True
        elif opt in "-f --force".split():
             force = True
        elif opt in "-g --group_name".split():
            group = arg
        elif opt in "-s --source_dir".split():
            source = arg
        elif opt in "-d --dest_dir".split():
            dest = arg
        elif opt in "-l --logfile".split():
            os.environ["LOGFILE"] = arg

    if (group is None) or (source is None) or (dest is None):
        sys.exit("Usage: group_mv -g <group_name> -s <source_dir> -d <dest_dir>")
    else:
        move_files(group, source, dest, recursive=recursive, overwrite=force)
    

if __name__ == "__main__":
   main()



