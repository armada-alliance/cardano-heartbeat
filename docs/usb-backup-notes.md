# Daily backup to stick

Daily backup of your cores hot keys and operational files to a local or remote usb stick with rsync.

## Source Disk Setup

### Log in and open a root shell

```bash
sudo su
```

Tail syslog before inserting your drive. This will print some information that can help you identify the disk.

```bash
tail -f /var/log/syslog
```

Attach the external drive and take note of the assigned device node. eg. /dev/sdb

> If the target drive is lacking partition tables syslog may not print the device node assignment. fdisk -l however will.

You can also print a list of drives with fdisk.

```bash
fdisk -l
```

Example output:

```bash
Disk /dev/sdb: 57.66 GiB, 61907927040 bytes, 120913920 sectors
Disk model: Cruzer
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: EECA81B9-3683-4A59-BC63-02EEDC04FD21
```

In my case it is /dev/sdb. Yours may be /dev/sdc, /dev/sdd or so on. /dev/sda is usually the system drive.
**<span style="color:red">Do not format your system drive by accident</span>**.

## Create an new GUID Partition Table (GPT)

**<span style="color:red">This will wipe the disk</span>**

```bash
gdisk /dev/sdb
```

Type ? to list options

```
Command (? for help): ?
b	back up GPT data to a file
c	change a partition's name
d	delete a partition
i	show detailed information on a partition
l	list known partition types
n	add a new partition
o	create a new empty GUID partition table (GPT)
p	print the partition table
q	quit without saving changes
r	recovery and transformation options (experts only)
s	sort partitions
t	change a partition's type code
v	verify disk
w	write table to disk and exit
x	extra functionality (experts only)
?	print this menu
```

1. Enter **o** for new GPT
2. Enter **n** to add a new partition and accept defaults to create a partition that spans the entire disk.
3. Enter **w** to write changes to disk and exit gdisk.

Your new partition can be found at /dev/sdb1, the first partition on sdb.

### Optionaly Check the drive for bad blocks (takes a couple of hours)

```bash
badblocks -c 10240 -s -w -t random -v /dev/sdb
```

## Format the partition as FAT32

Using FAT32 here because I know many users still use Windows or Mac OS as their local machine and a VPS for a core. EXT4 would be better if you run Linux locally and know you will not have to mount into Windows or MAC OS.

```bash
mkfs.fat -F 32 /dev/sdb1
```

## Mount the drive at boot

We want this drive to always be available to our backup job. Since it will be holding sensitive data we will mount it in a way where only root and the user cardano-node runs as can access.

Run blkid and pipe it through awk to get the UUID of the filesystem we just created.

```bash
sudo blkid /dev/sdb1 | awk -F'"' '{print $2}'
```

Example output:

```bash
748C-FBA1
```

For me the UUID=748C-FBA1

Drop back into your regular users shell.

```bash
exit
```

Add mount entry to the bottom of fstab adding your new partitions UUID and the full system path to your backup folder.
For this guide we set the path to a folder we will create in our home directory. /home/<username>/core-backup

Identify user id and group id and substitute for <xxxx> in fstab.

```bash
id $USER
```

```bash
sudo nano /etc/fstab
```

```bash
UUID=<748C-FBA1> /home/ada/core-backup vfat rw,uid=<xxxx>,gid=<xxxx>
```

> nofail allows the server to boot if the drive is not inserted.

Create the mountpoint & set default ACL for files and folders with umask.

```bash
cd; mkdir $HOME/core-backup; umask 022 $HOME/core-backup
```

Mount the drive.

```bash
sudo mount $HOME/core-backup
```

Take ownership of the filesystem.

```bash
sudo chown -R $USER:$USER $HOME/core-backup
```

Reboot the server and confirm the system mounted the drive at boot.

## Scheduled Backups

### Backup what you want with Rsync as frequently as you want.

Create a script that will only backup if the drive is mounted.

```bash
nano $HOME/core-backup-script.sh
```

```bash
#!/bin/bash
CNODE_HOME=$NODE_HOME
# Local Source
#SOURCE="$NODE_HOME"
# Remote Source
REMOTE_SOURCE="-i -e "ssh -i $HOME/.ssh/<private key>" <user>@<server name or IP>:$NODE_HOME"
DESTINATION="$HOME/core-backup/"

if grep -qs "$HOME/core-backup" /proc/mounts; then
   echo "Executing Rsync"
   rsync -av --exclude-from="exclude-list.txt" $SOURCE $DESTINATION
else
   echo "Core backup drive is not mounted."
fi
exit 0

```

```bash
chmod +x $HOME/core-backup-script.sh
```

Create an rsync-exclude.txt file so we can rip through and grab everything we need and skip the rest.

```bash
cd; nano exclude-list.txt
```

```bash
.bash_history
.bash_logout
.bashrc
.cache
.config
.local/bin/cardano-node
.local/bin/cardano-service
.profile
.selected_editor
.ssh
.sudo_as_admin_successful
.wget-hsts
git
tmp
pi-pool/db
pi-pool/scripts
pi-pool/logs
usb-transfer
core-backup-script.sh
exclude-list.txt
```

### Setup Cron

Open crontab and add the rule to the bottom.

```bash
crontab -e
```

```bash
# Replace with correct path to your pools working directory
#
# run 3am every day
0 3 * * * $HOME/core-backup-script.sh
```

## Optional backup alias with mount check

Create an alias in .bashrc or .adaenv if present for manual alias to backup the core.

```bash
cd; nano .bashrc
```

Add the following at the bottom edit the paths and exclude as you see fit and source the changes.

```bash
if grep -qs '$HOME/core-backup ' /proc/mounts; then
    echo "Core backup drive is mounted. Executing Rsync"; alias core-backup="rsync -a --exclude={"db/","scripts/","logs/"} $NODE_HOME $HOME/core-backup/"
else
    echo "Core backup drive is not mounted."
fi
exit 0

```

```bash
source .bashrc
```
Now if you want to manually backup the hot keys just type core-backup. For example after generating a new KES pair and node.cert

```bash
core-backup
```