# Daily backup to stick

Daily backup of your cores hot keys and operational files to a local or remote usb stick with rsync.

Auto mount by UUID to users home folder with an alias that moves the relays operational files out of the way, copies hot keys and files into place and restarts the relay as your core.

### Considerations
With remote backup keeping hot keys off relay till needed. Most likely with a 'backup' user without shell access and chroot

[Remote Security](https://stackoverflow.com/a/63462199)


This will likely have to be two sets of instructions based on whether this is baremetal(can we only cater to winners?) behind a router NAT or a vps core(with wiregaurd) which will require extra security since datacenter system admins shoud not be afforded shell access to the backup stick and should not be able to discern the filesystem tree either.

