# YAMLProxy

YAMLProxy is a simple HTTP reverse proxy server that uses YAML configuration for routing. It allows you to configure routes for different backend applications and handle custom error pages.

## Features

- Reverse proxy HTTP requests based on YAML configuration.
- Automatic stripping of prefixes from the request path.
- Handling of relative redirects from proxied applications.
- Custom error pages for different routes.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- PyYAML

Install dependencies:

```bash
pip install Flask pyyaml
```
### Configuration
Edit the proxy_config.yaml file to configure routes, destinations, and optional error pages:
```yaml
routes:
  - path: /app1
    destination: http://localhost:8001
  - path: /app2
    destination: http://localhost:8002
errors:
  - status_code: 404
    page: _internal/404.html

  - status_code: 500
    page: _internal/500.html
```
### Installation
You can either build the system from source:
```sh
git clone https://github.com/stupidjohanna/yamlgate && cd yamlgate
git fetch upstream
git pull
```
And install:
```sh
make update # Download the latest Version
make install_reqs # Download all required Libraries
sudo make sys_install # Installs the System to /usr/bin/yamlgate
sudo make systemd_install # OPTIONAL: Turns YAMLGate into a Daemon

```

Or use the one-line install:

`curl https://raw.githubusercontent.com/StupidJohanna/YAMLGate/master/jumpstart.sh | sh`

If you happen to have [Nixoid](https://github.com/stupidJohanna/nixoid) installed, you can run
`nixoid install stupidjohanna/YAMLGate-nixoid-light`

The server will run on http://0.0.0.0:80 

### Running Minimalistic Apps
Run minimalistic apps for testing:
`python example.py`
Access the app through the proxy:
* http://localhost/app1
### Handling Error Pages
* **404 Not Found**:
    The user-friendly 404 page is displayed, suggesting users contact the website owner for assistance. For website owners, it provides guidance on checking configurations and server logs.

* **500 Internal Server Error**:
    The user-friendly 500 page is displayed, informing users of a server error and suggesting they try again later. For website owners, it provides guidance on checking server logs and reviewing recent changes.
