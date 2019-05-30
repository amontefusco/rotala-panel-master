## How to install systemd services

	sudo cp rotala* /etc/systemd/system/

stop the old services (if any)

  	sudo systemctl daemon-reload
  	sudo systemctl stop chromium savescreen rotala


Check that the services are really there

	systemctl list-unit-files rotala*

Enable the services:

	sudo systemctl enable rotala*

Start the group

	sudo systemctl start rotala

Check 

	systemctl status rotala*




