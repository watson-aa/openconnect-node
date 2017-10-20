# openconnect-node
**NodeJS wrapper for OpenConnect VPN client**

Default config file should be in *~/.config/network/openconnect.config*

**Prequisites:**

[Homebrew](https://brew.sh/)

*brew install openconnect*


For RSA token:

*brew install stoken*

*stoken import --file=foo.sdtid*

*stoken setpin*


To run:

*sudo openconnect.py VPN_NAME [CONFIG_FILE]*

Config file must be valid JSON.  See openconnect.config for an example


Valid VPN authentication types are *basic*, which requires at least one username and password, and *stoken*, which requires a configured RSA certificate and pin.
