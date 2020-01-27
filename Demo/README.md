# Demonstration

> Demo of the MITM Proxy on a Raspberry Pi 3 B+

## Configuration

*Setup the Raspberry Pi 3 B+ by completing the following steps*

### 1. Burn the ISO

*The ShmooCon demo and the steps below used the `2019-09-26-raspbian-buster-full` ISO.*

### 2. First Boot

1. *If you plan on ever using the desktop environment*, complete the locale and basic setup using the GUI, otherwise use `raspi-config` to set your locale settings.
2. *If you plan on working from another host*, enable SSH before you reboot using `sudo systemctl enable ssh`.
3. Reboot with `reboot` and SSH in from your primary machine if desired.
4. Update, upgrade, and install the required packages using the below commands in the terminal:

```bash
sudo apt update
sudo apt dist-upgrade -y
sudo apt install -y isc-dhcp-server hostapd
```

5. Complete the following steps to configure your DHCP client:

```bash
# disable wlan0
sudo ifdown /dev/wlan0

# add dhcpcd entry for wlan0
echo -e 'interface wlan0\n    static ip_address=172.16.0.1/24\n    nohook wpa_supplicant' | sudo tee -a /etc/dhcpcd.conf

# restart the updated services
sudo systemctl restart dhcpcd
```

6. Complete the following steps to configure your DHCP server:

```bash
# set wlan0 as the dhcp interface
sudo sed -i 's/INTERFACESv4=""/INTERFACESv4="wlan0"/g' /etc/default/isc-dhcp-server

# get a basic config for dhcpd
sudo wget -O /etc/dhcp/dhcpd.conf https://raw.githubusercontent.com/usma-eecs/mobile-app-privacy-score/master/Demo/dhcpd.conf

# restart the service
sudo systemctl restart isc-dhcp-server

# verify
systemctl status isc-dhcp-server

# troubleshoot as necessary
sudo cat /var/log/syslog | grep isc-dhcp-server
# make changes
sudo systemctl restart isc-dhcp-server
# return to verify above
```

7. Complete the following steps to configure your AP:

```bash
# point the apd at the correct config file
sudo sed -i 's|#DAEMON_CONF.*|DAEMON_CONF="/etc/hostapd/hostapd.conf"|g' /etc/default/hostapd

# get a basic config for hostapd
sudo wget -O /etc/hostapd/hostapd.conf https://raw.githubusercontent.com/usma-eecs/mobile-app-privacy-score/master/Demo/hostapd.conf

# start the ap
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

# verify
systemctl status hostapd

# troubleshoot as necessary
sudo cat /var/log/syslog | grep hostapd
# make changes
sudo systemctl restart hostapd
# return to verify above
```

8. Complete the follow steps to allow routing from eth to wlan:

```bash
# enable forwarding
sudo sed -i 's/.*net.ipv4.ip_forward.*/net.ipv4.ip_forward=1/g' /etc/sysctl.conf
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

# firewall forwarding
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo nano /etc/rc.local
# add before exit 0
iptables-restore < /etc/iptables.ipv4.nat

```

9. Currently `isc-dhcp-server` and `hostapd` are starting out of order, to fix, follow the below steps:

```bash
# run these on login
sudo systemctl restart isc-dhcp-server.service 
sudo systemctl restart hostapd
```
