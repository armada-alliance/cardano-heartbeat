# SPO Backup Plan Basics

Many small SPOs dream of their first block. Then after that block shows up a weight is lifted and the real fun begins, like waiting to pull those first rewards. 
But how many SPOs dream about a backup plan? You've tweaked your pool and she's purring like a lambo on the autobahn. So what could go wrong? And if something does, would you know how to recover? Well, stop staring at your pool metrics and lets explore some basic backup plan options using the 3-2-1 methodology.

### What Could Go Wrong?

A better question to ask is when. Anything could go wrong and if it impacts your pool it's a big deal. You gotta be ready to deal with it as quickly as possible given the circumstances at hand. Your next block is in 1 hour and you just lost your core node, GO!

***What types of disruptions can cause emergencies?***

- Natural Disaster

- War or Terrorism

- Civil Disruption or unrest

- Accidents or human error

- Cyber Attacks

***What are the most important points of failure to an SPO?***

1. Power
2. Internet outages
3. Network
4. Critical operational Data, secret keys, and files
5. Human error


### What is a 3-2-1 Backup Plan?

![](/.gitbook/assets/3-2-1-backup.png)

Simple, 3 copies of all your stuff where 2 copies are on two different media types and one copy is completely offsite. This 3-2-1 backup plan is a great way to keep your Stake Pool and its essential data safe.

#### **3 Copies of Data**

Following this 3-2-1 plan we have three distinct copies of our stake pool's operational/production data. With one copy being the current data used for stake pool operation purposes (i.e., keys, certs, metadata, wallets, etc...). The other two copies are backups of the pool's operational data.

An important aspect in keeping your pool's data safe and recoverable is for all three copies of the data (operational and the two backups) to be stored in such a manner that if one or more of the copies should fail/lost you always have another copy safe and intact to recover from. 

Lastly, it is vital to make sure all your data copies are all updated and kept in sync with the current operational data being used, do not update one copy and leave the other two out of sync. For example if you update the current operational data and leave the backup out of sync you will not be able to recover your stake pool in case of a crisis. All copies should contain the same data from the same exact point in time.

#### **2 Media Types**

For the two backup copies we use two different media types. One is a hard drive and the other is a cloud based storage. That way we can be sure if one of the copies is lost or fails we can still recover from it. It is recommend to keep the cloud based backup located in a different region not near your other local copies.

#### **1 Offsite Location**

In general, offsite means remotely. However, it is safe enough if you can keep at least 1 backup stored in another place long distance, i.e. not onsite. Hard drive devices fail eventually, so a perfect place for offsite would be cloud drive, NAS or network share.

Physical storages may be damaged by human error, flood, earthquake, or stolen by theft, but that is hardly appear on network drives especially on the cloud storage that offered by well-known service providers. Believe it or not, they have more strict ways to ensure data security.

### Why Do I Need A Plan?

Sure you can be _that guy or gal_, but your introducing a lot of risk. The goal is to minimize downtime and risk. The longer your pool is down the more risk you have of missing a block or the longer it'll take to sync back up to the chain. Once you're sitting on a solid plan you can use it to your pool's advantage. Advertise it as a means to draw delegates. Share your plan in your circle of influence so others can benefit as well. A good decentralized blockchain needs SPOs who are serious about minimizing downtime.

### What Should I Backup?


What files are important to an SPO to recover from a crisis?

{% tabs %}
{% tab title="KEYS/Files for the Pool" %}
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

{% endtab %}
{% tab title="Configuration files" %}

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


{% endtab %}
{% tab title="Cardano Node, Monitoring, and dev tools" %}

- Binaries
	- cardano-cli
	- cardano-node

- Tools and Monitoring 
	- gLiveView.sh
	- env
	- cardano-service (armada alliance optional)
	- armadaPing.sh (armada alliance optional)
	- topologyUpdater.sh

{% endtab %}
{% endtabs %}


### How Should I Backup?



### Where Should I Backup?

We suggest that you use the hybrid backup plan model.


### How To Recover?


| References   								 	 |
|------------------------------------------------------------------------------  |
| [Jeff Greenling's Backup Plan](https://github.com/geerlingguy/my-backup-plan)  |  
| [msp360.com](https://www.msp360.com/resources/blog/data-backup-plan/)   |