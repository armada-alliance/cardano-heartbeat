#These functions return exit codes: 0 = found, 1 = not found

isMounted    () { findmnt -rno SOURCE,TARGET "$1" >/dev/null;} #path or device
isDevMounted () { findmnt -rno SOURCE        "$1" >/dev/null;} #device only
isPathMounted() { findmnt -rno        TARGET "$1" >/dev/null;} #path   only

#where: -r = --raw, -n = --noheadings, -o = --output

if isPathMounted "/mnt/foo bar";      #Spaces in path names are ok.
   then echo "path is mounted"
   else echo "path is not mounted"
fi

if isDevMounted "/dev/sdb4"; 
   then echo "device is mounted"
   else echo "device is not mounted"
fi

#Universal:
if isMounted "/mnt/foo bar"; 
   then echo "device is mounted"
   else echo "device is not mounted"
fi

if isMounted "/dev/sdb4";
   then echo "device is mounted"
   else echo "device is not mounted"
fi
