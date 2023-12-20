echo "Receiving latest Version..."
git clone https://github.com/StupidJohanna/YAMLGate
cd YAMLGate
pip install -q -U flask werkzeug pyyaml
rm -rfv /usr/bin/yamlgate
mkdir /usr/bin/yamlgate
cp -r . /usr/bin/yamlgate
echo "Do you want to install YAMLGate as a Systemd Service? (Y/n): "
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    cp services/yamlgate.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable yamlgate.service
    systemctl start yamlgate.service
else
    echo "You chose not to proceed."
fi