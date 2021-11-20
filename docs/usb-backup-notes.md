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

>If the target drive is lacking partition tables syslog may not print the device node assignment. fdisk -l however will.

You can also a list of drives with fdisk.

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
1. Enter o for new GPT
2. Enter n to add a new partition and accept defaults to create a partition that spans the entire disk.
3. Enter w to write changes to disk and exit gdisk.

Your new partition can be found at /dev/sdb1, the first partition on sdb.

 ### Optionaly Check the drive for bad blocks (takes a couple of hours)

 ```bash
 badblocks -c 10240 -s -w -t random -v /dev/sdb
  ```

## Format the partition as ext4
We still need to create a filesystem on the partition.

```bash
mkfs.ext4 /dev/sdb1
```

Example output:

```bash

mke2fs 1.46.3 (27-Jul-2021)
Creating filesystem with 15113979 4k blocks and 3784704 inodes
Filesystem UUID: 56c1fa6c-5f41-4d48-b985-89b02893f67a
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
	4096000, 7962624, 11239424

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (65536 blocks): done
Writing superblocks and filesystem accounting information: done   
```
## Mount the drive for $USER at boot
We want this drive to always be available to our backup script. Since it will be holding sensitive data we will mount it in a way where only root and the user cardano-node runs as can access.

Run blkid to get the UUID of the filesystem we just created.

```bash
sudo blkid /dev/sdb1 | awk -F'"' '{print $2}'
```
Example output:

```bash
56c1fa6c-5f41-4d48-b985-89b02893f67a
```
For me the UUID=56c1fa6c-5f41-4d48-b985-89b02893f67a

Drop back into your regular users shell.

```bash
exit
```
Add mount entry to the bottom of fstab adding your UUID and the full system path to you backup folder.

```bash
sudo nano /etc/fstab
```

```bash
UUID=12ce4f16-1f2a-42aa-9783-f9e1c229b16e <full path to mount> auto defaults,nofail 0 1
```

>nofail allows the server to boot if the drive is not inserted.

```bash
cd ; mkdir $NODE_HOME/backup
```
Take ownership of the drive.

```bash
sudo chown -R $USER:$USER $NODE_HOME/backup
```

Test the mount.

```bash
sudo mount $NODE_HOME/backup
```


