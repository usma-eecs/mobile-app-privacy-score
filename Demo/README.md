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

5. Complete the following steps to configure your DHCP server:

```bash
# disable wlan0
ifdown /dev/wlan0

# set wlan0 as the dhcp interface
sudo sed -i 's/INTERFACESv4=""/INTERFACESv4="wlan0"/g' /etc/default/isc-dhcp-server


```
