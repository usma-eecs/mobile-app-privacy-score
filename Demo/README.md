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
# can now connect to the raspberry pi's Wi-Fi
```

### 3. MITMproxy Setup

1. MITMproxy installation for Debian 10 (buster)

```bash
# see https://mitmproxy.readthedocs.io/en/v2.0.2/install.html for installation for a different OS
sudo apt-get install python3-dev python3-pip libffi-dev libssl-dev
sudo pip3 install mitmproxy
```

2. Install MITMproxy certificate on your Apple device

```bash
# MITMproxy will automatically generate a certificate authority when mitmdump or mitmproxy is run for the first time
mitmdump
# wait until Proxy server listening at http://*:8080 comes up
```
- Get the certificate from your proxy server at /.mitmproxy/mitmproxy-ca-cert.pem
- Transfer the certificate to the Apple device you would like to mitm. In this case, I sent the file over Slack because I have the app installed on both my laptop and iPhone
- On your Apple Device:
  - Open the CA file in a browser.
  - When the file opens in the browser, you will be prompted by "This website is trying to download a configuration profile. Do you want to allow this?" Click "Allow" and then "Close" for the next prompt.
  - Go to Settings > General > Profiles & Device Management. Under "Downloaded Profile" click "mitmproxy." In the top right corner, click "install." Enter your passcode when prompted and then click "install."
  - Go to Settings > General > About > Certificate Trust Settings. Enable full trust for "mitmproxy."

3. Set up for a SOCKS5 Proxy

*The proxy for this demo is run in SOCKS5 mode*

- Create a .pac file inside of the git repository
- Code within the .pac file is as follows:

 ```bash
 function FindProxyForURL(url, host)
{
    return "SOCKS 192.168.137.106:8080";
    #the address above should be the eth0 IPv4 address of the raspberry pi
}
 ```
 - View the file on github using the "raw" option
 - Copy the link to the file, in this case the link is https://raw.githubusercontent.com/usma-eecs/mobile-app-privacy-score/b9ef47fe9f11729419253ba994059a290a3ee00c/proxy.pac
 - On your Apple device:
    - Go to settings > Wi-Fi > the info button next to the raspberry pi's Wi-Fi > Configure Proxy. Select automatic and insert the URL to the .pac file.
    - Save it

4. Running MITMproxy

- Go to raspberry pi
```bash
mitmdump -m socks5 -w outfile
# outfile can be replaced with any name of file captured traffic will be written to
# Can easily overwrite old outfiles so be careful not to use the same name twice
```
- Attempt to access the internet through an app on the Apple Device
- Network traffic should be seen in the terminal
