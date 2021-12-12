# Alliance Microk8's Cluster Build

High availabilty Microk8's cluster with optional multi NIC failover with OpenWRT/Quagga

## Flash Ubuntu 20.10 Image

Create a user and setup server.

```bash
sudo adduser ada; sudo adduser ada sudo
```

Delete ubuntu user.

```bash
sudo deluser --remove-home ubuntu
```

Update the server, reboot and install linux-modules-extra-raspi, reboot again. Server may not reboot without unplugging(hang). Subsequent reboots are fine.

```bash
sudo apt update; sudo apt upgrade -y
reboot
```

Extra packages needed for for Raspi.

```bash
sudo apt install linux-modules-extra-raspi chrony zram-config rng-tools
```

Overclock to 2ghz.

```bash
sudo nano /boot/firmware/config.txt
```

```bash
over_voltage=6
arm_freq=2000
gpu_mem=16
disable-wifi
disable-bt
```

Reboot.

### Enable memory cgroups, ensure legacy IP tables.

```bash
sudo nano /boot/firmware/cmdline.txt
## Add the following options at the beginning
cgroup_enable=memory cgroup_memory=1
```

Modern linux distributions use nftables the current kubeadm is not compatible with nftables, it causes duplicate firewall rules and breaks kube-proxy. Change the iptables tooling to legacy mode.

```bash
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
```

### Enable forwarding and bridging between interfaces.

```bash
sudo nano /etc/sysctl.conf
```

Add to the bottom.

```
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
```

Load them at boot.

```bash
sudo nano /etc/rc.local
```

```bash
#!/bin/bash

# Give CPU startup routines time to settle.
sleep 120

sysctl -p /etc/sysctl.conf

exit 0
```

Empty apt cache and reboot for the hell of it.

```
sudo apt clean
reboot
```

# Create an image from here to save time.

It is worth creating an image you can burn here to save time.

[create an img to burn](https://docs.armada-alliance.com/learn/cardano-developer-guides/create-.img-file)

# Configure Hostname & Static ip

Configure hostname and static IP on all the nodes.

# Install Microk8's

```bash
sudo snap install microk8s --classic
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
su - $USER
```

Alias

```bash
nano .bashrc
```
add to bottom.

```
alias kubectl='microk8s kubectl'
```

## Enable Addons

```bash
microk8s enable dns storage ingress metallb:192.168.254.0/24
```

Create an ingress service. Log into your first node and create a service file and apply it. Here I am making a directory to hold my cluster files.

```bash
mkdir cluster-configs
cd cluster-configs/
nano ingress-service.yaml
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ingress
  namespace: ingress
spec:
  selector:
    name: nginx-ingress-microk8s
  type: LoadBalancer
  # loadBalancerIP is optional. MetalLB will automatically allocate an IP
  # from its pool if not specified. You can also specify one manually.
  # loadBalancerIP: x.y.z.a
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
    - name: https
      protocol: TCP
      port: 443
      targetPort: 443
```

```bash
kubectl apply -f ingress-service.yaml
```

### Inspect the node for problems.

```bash
microk8s inspect
```

> If you see any problems with iptables or cgroups you can try purge remove and reinstall.

### Repeat this on all nodes intended for the cluster.

# Connect local machines kubectl to cluster

On your local machine install kubectl

```
snap install kubectl --classic
kubectl version --client
```

Create a .kube.config by copying the clusters config to your local machine. You can print the config out from one of the cluster machines terminal.

```
microk8s config
```

Copy all of it into a file on your local machine.

```
cd; nano .kube/config
```

Confirm it can connect to your cluster

```
kubectl cluster-info
```

### Kubectl Bash Completion

```
# setup autocomplete in bash into the current shell, bash-completion apt package should be installed first.
source <(kubectl completion bash)
# add autocomplete permanently to your bash shell.
echo "source <(kubectl completion bash)" >> ~/.bashrc
```

# True Network Load Balancing with BGP

Setup Microk8's load balancing with MetalLB & BGP routing on OpenWRT with Quagga.

### Two core features of MetalLB:

MetalLB basically deploys 2 components:

> metallb-system/controller, Responsible for the allocation of IP addresses, and monitoring of service and endpoint

> metallb-system/speaker, Responsible for ensuring that the service address is reachable, for example, in Layer 2 mode, the speaker will be responsible for ARP request response.

Note that after deployment, you also need to configure ConfigMap according to the specific address notification method in metallb-system/config. The controller will read the configmap and reload the configuration.

## Address allocation

MetalLB will assign an IP address to the user's load balancer ingress service. The IP address is not generated out of thin air and needs to be allocated in advance by the user.

### External statement

After the address is assigned, it needs to be notified to other hosts in the network. MetalLB supports two declaration modes:

1. ARP/NDP
2. BGP

## Layer 2 mode: ARP/NDP

In Layer 2 mode, each service will have a node in the cluster to be responsible. When the service client initiates ARP resolution, the corresponding node will respond to the ARP request. After that, the traffic of the service will be directed to the node (it seems that there are multiple addresses on the node).

Layer 2 mode is not true load balancing, because traffic will pass through one node first, and then forwarded to multiple end points through the ingress controller. If that node fails, MetalLB will migrate the IP to another node and resend the free ARP to inform the client to migrate. Modern operating systems can basically handle gratuitous ARP correctly, so failover will not cause much problem.

Layer 2 mode is more general and does not require users to have additional equipment, but because Layer 2 mode uses ARP/NDP, the address pool allocation needs to be on the same subnet as the client, and address allocation is cumbersome.

## BGP mode

In BGP mode, all nodes in the cluster will establish a BGP connection with the uplink router, and will tell the router how to forward service traffic. In ARP mode you have to allocate IP's from your LAN for use.

With BGP, MetalLB can route to different subnets as announced. Allowing the router to hold all physical NIC's in it's routing table should one go down the next route in will be used.

# Configure OpenWRT

There must be an uplink switch that can run the BGP protocol.

OpenWRT can run Quagga. Quagga is a classic routing software suite under the unix platform, which implements the following routing protocols: OSPFv2, OSPFv3, RIP v1 and v2, RIPng and BGP-4.

We will use the bgp function of Quagga to complete the BGP mode deployment of MetalLB.

# **BGP mode is a real Load Balancer.**

## Install Quagga on OpenWRT

Install Quagga, dependencies & tools for management.

```bash
opkg update
opkg install quagga quagga-zebra quagga-bgpd quagga-watchquagga quagga-vtysh
```

Start Quagga, and it will monitor ports 2601, 2605 and 179.

```bash
/etc/init.d/quagga start
/etc/init.d/quagga enable

netstat -antp|grep LISTEN
tcp        0      0 0.0.0.0:2601            0.0.0.0:*               LISTEN      23173/zebra
tcp        0      0 0.0.0.0:2605            0.0.0.0:*               LISTEN      23178/bgpd
tcp        0      0 0.0.0.0:179             0.0.0.0:*               LISTEN      23178/bgpd
```

## Configure BGP protocol on OpenWRT

OpenWRT will establish a BGP peer pair with each node on kubernetes. Here, we set the ASN of OpenWRT to 65000 and the ASN of each node on kubernetes to 65001.

After logging in to OpenWrt with ssh use the 'vtysh' command to enter Quagga's command line. Add each of your nodes. You need atleast 3 nodes for high availability. The configuration is as follows.

```bash
vtysh
configure terminal
(config)# router bgp 65000
(config-router)# neighbor 192.168.1.200 remote-as 65001
(config-router)# neighbor 192.168.1.200 description "node-0"
(config-router)# neighbor 192.168.1.201 remote-as 65001
(config-router)# neighbor 192.168.1.201 description "node-1"
(config-router)# neighbor 192.168.1.202 remote-as 65001
(config-router)# neighbor 192.168.1.202 description "node-2"
exit
exit
write file
exit
```

Write file will save the configuration into /etc/quagga directory.

BGP on OpenWRT is now configured, and the routing information of each node on kubernetes needs to be configured.

## Configure BGP protocol on kubernetes

Log into your first node again and create and apply a metallb-configmap.yaml file to enable BGP on MetalLB.

```
cd cluster-configs/
nano metallb-configmap.yaml
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    peers:
    - peer-address: 192.168.1.1
      peer-asn: 65000
      my-asn: 65001
    address-pools:
    - name: default
      protocol: bgp
      addresses:
      #- 192.168.1.10-192.168.1.100
      - 192.168.254.0/32
```

```bash
kubectl apply -f metallb-configmap.yaml
```
MetalLB will not apply breaking changes so we need to delete the speaker pods it created when we enabled it. It will recreate new ones that will work with our new ConfigMap.

Delete the controller and speaker pods, when they come back up we should have BGP routes

```
kubectl delete po -n metallb-system --all
```

Back in OpenWRT look at the current BGP status.

```
vtysh
show ip bgp summary
Hello, this is Quagga (version 1.1.1).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

openwrt# show ip bgp summary
BGP router identifier 192.168.1.1, local AS number 65000
RIB entries 1, using 72 bytes of memory
Peers 3, using 14 KiB of memory

Neighbor        V         AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
192.168.1.200   4 65001    5741    5748        0    0    0 1d23h36m        1
192.168.1.201   4 65001    5712    5716        0    0    0 1d23h35m        1
192.168.1.202   4 65001    5735    5746        0    0    0 1d23h15m        1

Total number of neighbors 3
```

After the controller restarts the reassigned address for the previous svc nginx is 192.168.254.0 Let's take a look at the routing table entries on OpenWRT.

```bash
OpenWrt# show ip route
Codes: K - kernel route, C - connected, S - static, R - RIP,
       O - OSPF, I - IS-IS, B - BGP, P - PIM, A - Babel,
       > - selected route, * - FIB route

K>* 0.0.0.0/0 via 24.60.52.1, eth2, src 24.60.55.219
C>* 10.111.222.0/24 is directly connected, br-guest_turris
C>* 24.60.52.0/22 is directly connected, eth2
C>* 127.0.0.0/8 is directly connected, lo
C>* 192.168.1.0/24 is directly connected, br-lan
B>* 192.168.254.0/32 [20/0] via 192.168.1.200, br-lan, 1d23h19m

```

As you can see, the last one is a BGP route and 192.168.254.0/32 packets will be forwarded to 192.168.1.200. when you visit on the client browser, the 192.168.254.0 Nginx page will be displayed (the default route of the client is the IP address of OpenWRT 192.168.1.1).

### BGP mode analysis

Let's analyze the BGP mode below.

Since the default route of the client is the IP of OpenWRT 192.168.1.1, when the browser visits 192.168.254.0 the message will be sent to OpenWRT.

Check the BGP route on OpenWRT, Next Hop hits 192.168.1.200, OpenWRT forwards the message to 192.168.1.200.

After the message arrives 192.168.1.200, it will hit the iptables rule and forward the message to the EndPoint of the actual pod. The subsequent process is similar to the general access to svc.

After the message is forwarded by the router, it is actually forwarded by a node on kubernetes within the cluster, which is similar to the Layer 2 mode.

### failover

So, what if it 192.168.1.200 fails? Let's check the bgp routing on the Omnia in detail.

```bash
OpenWrt# show ip bgp
BGP table version is 0, local router ID is 192.168.1.1
Status codes: s suppressed, d damped, h history, * valid, > best, = multipath,
              i internal, r RIB-failure, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*  192.168.254.0/32 192.168.1.202                          0 65001 ?
*                   192.168.1.201                          0 65001 ?
*>                  192.168.1.200                          0 65001 ?

Displayed  1 out of 3 total prefixes

```

The actual Next Hop includes all the nodes of kubernetes, but currently only one (that is, the > pointed entry) is used; when a 192.168.1.200 fails, BGP will quickly switch to another Hop to complete the failover.

## Summary

In practical applications if the conditions are met it is recommended to use BGP mode.

[At home with Kubernetes, MetalLB and BGP](https://www.growse.com/2019/04/13/at-home-with-kubernetes-metallb-and-bgp.html)

[MetalLB Config Page](https://metallb.universe.tf/configuration/)

[cgroup heirarchy](https://github.com/ubuntu/microk8s/issues/1691#issuecomment-977543458)

[some clues](https://dev.to/musabhusaini/remote-development-with-multi-node-microk8s-cluster-and-scaffold-4o1d)

[Rebuild existing services](https://github.com/metallb/metallb/issues/348)
