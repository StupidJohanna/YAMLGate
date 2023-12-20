all:

	make update
	make install_reqs

update:
	echo "Receiving latest Version..."
	git fetch
	git pull

install_reqs:
	pip install -q -U flask werkzeug pyyaml

sys_install:
	mkdir /usr/bin/yamlgate
	cp -r . /usr/bin/yamlgate
systemd_install:
	cp services/yamlgate.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl enable yamlgate.service
	systemctl start yamlgate.service