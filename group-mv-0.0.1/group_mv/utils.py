from .logger import Logger
import os
import grp
import pwd


# group name to list of group member uids
_grname2uids = {g.gr_name: [pwd.getpwnam(user).pw_uid for user in g.gr_mem] 
                    for g in grp.getgrall()}

# append primary group user's uid
for user in pwd.getpwall():
    uid,gid = user.pw_uid, user.pw_gid
    _grname2uids[grp.getgrgid(gid).gr_name].append(uid)


def _is_target(file_path, group):
    "Returns whether owner of file in `file_path` is member of `group`"
    f_info = os.stat(file_path)
    owner_uid = f_info.st_uid
    try:
        member_uids = _grname2uids[group]
    except:
        raise Exception(f"Group does not exist: {group}")
    return owner_uid in member_uids

    
@Logger.log_decorator
def move_files(group, source, dest, recursive=False, overwrite=False):
    """Move files located in `source` to `dest` if file owner is member of `group`, 
    optionally recursive and with overwriting in `dest`"""

    # set absolute path if path is relative
    if not os.path.isabs(source):
        source = os.path.join(os.getcwd(), os.path.relpath(source)) 
    if not os.path.isabs(dest):
        dest = os.path.join(os.getcwd(), os.path.relpath(dest)) 
     
    # get files in directory and optionally files in subdirs
    if recursive:
        files = []
        for r,_,f in os.walk(source):
            for fn in f:
                file = os.path.join(r, fn)
                if _is_target(file, group):
                    files.append(file)
    else:
        files = [os.path.join(source,f) for f in os.listdir(source) 
                    if os.path.isfile(os.path.join(source,f)) and _is_target(os.path.join(source,f), group)]

    # filenames in dest folder
    dest_files = [f for f in os.listdir(dest) if os.path.isfile(os.path.join(dest,f))]

    # remove files from list which would overwrite files in dest
    if not overwrite:
        no_move = [f for f in files if os.path.basename(f) in dest_files]
        files = [f for f in files if f not in no_move]
        n = len(no_move)
        if n > 0:
            print(f"Unable to move {n} {'file' if n==1 else 'files'} from {source} to {dest}")
            print("Use parameter -f, --force to overwrite files in destination folder")

    # move files
    n = len(files)
    if n > 0:
        print(f"Moving {n} {'file' if n==1 else 'files'} from {source} to {dest}")
        for f in files:
            os.rename(f, os.path.join(dest, os.path.basename(f)))
    else:
        print("No files to move")
