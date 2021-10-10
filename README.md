# group_mv
Moves files owned by users of a specified group from source to destination folder.

Usage: `group_mv -g <group_name> -s <source_dir> -d <dest_dir>`

Required parameters:
* `-g, --group_name <GROUP NAME>`
* `-s, --source_dir <SOURCE FOLDER>`
* `-d, --dest_dir <DESTINATION FOLDER>`

Optional parameters:
* `-r, --recursive         move files of source folder and files in subdirectories`
* `-f, --force             overwrite files in destination folder`
* `-l, --logfile <LOGFILE> use a custom logfile`

Build:

```
sudo apt-get update && apt-get install dpkg-dev devscripts fakeroot
git clone https://github.com/rbrtwlz/group_mv
cd group_mv/group-mv-0.0.1
dpkg-buildpackage -b -uc -us
sudo dpkg -i ../python3-group-mv_0.0.1-1_all.deb 
group_mv --help```
