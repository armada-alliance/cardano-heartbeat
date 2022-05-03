# SPO Backup Plan Basics

Many small SPOs dream of their first block. Then after that block shows up a weight is lifted and the real fun begins, like waiting to pull those first rewards. 
But how many SPOs dream about a backup plan? You've tweaked your pool and she's purring like a lambo on the autobahn. So what could go wrong? And if something does, would you know how to recover? Well, stop staring at your pool metrics and lets explore some basic backup plan options using the 3-2-1 methodology.

### What Could Go Wrong?

A better question to ask is when. Anything could go wrong and if it impacts your pool it's a big deal. You gotta be ready to deal with it as quickly as possible given the circumstances at hand. Your next block is in 1 hour and you just lost your core node, GO!

### What is a 3-2-1 Backup Plan?

Simple: 3 copies of all your stuff where 2 copies are on two different media types and one copy is completely offsite.

### Why Do I Need A Plan?

Sure you can be _that guy or gal_, but your introducing a lot of risk. The goal is to minimize downtime and risk. The longer your pool is down the more risk you have of missing a block or the longer it'll take to sync back up to the chain. Once you're sitting on a solid plan you can use it to your pool's advantage. Advertise it as a means to draw delegates. Share your plan in your circle of influence so others can benefit as well. A good decentralized blockchain needs SPOs who are serious about minimizing downtime.

### What Should I Backup?


What files are important to an SPO to recover from a crisis?

- KEYS/Files for the Pool
	- Node.vkey (cold)
	- Node.skey (cold)
	- Node.opcert.counter (cold)
	- Node.kes.vkey (hot)
	- Node.kes.skey (cold)
	- Node.opcert (hot)
	- Node.vrf.vkey (cold)
	- Node.vrf.skey (cold)
	- Payment.vkey (cold)
	- Payment.skey (cold)
	- Stake.vkey (cold)
	- Stake.skey (cold)
	- Stake.address 
	- Payment.address (hot)
	- Stake.cert (hot)
	- Metadata.json 
	- poolMetadataHash.txt 
	- MetadataUrl
	- Pool.registration.cert
	- Deleg.cert (hot)

- DB snapshot (backup)

- Network Configs
	- ufw/iptables
		- sudo ufw status numbered
		- sudo iptables -S
	- wireguard config
		- /etc/wireguard/wg0.conf
		- /root/wg
	- Router config/snapshot

- Pool Configs
	- mainnet-config.json
	- mainnet-alonzo-genesis.json
	- Mainnet-byron-genesis.json
	- mainnet-shelley-genesis.json
	- mainnet-topology.json
- Binaries
	- cardano-cli
	- cardano-node


- Tools and Monitoring 
	- gLiveView.sh
	- env
	- cardano-service (armada alliance optional)
	- armadaPing.sh (armada alliance optional)
	- topologyUpdater.sh


### How Should I Backup?

### Where Should I Backup?

### How To Recover?
