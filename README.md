# Prometheus Exporter Installer
### This automation will:
* Download the exporter on a (unix) server
  * validate sha
* Install the exporter
* configure the exporter
* set it up as a service
* clean up


Need tests. 

### References
* https://www.digitalocean.com/community/tutorials/how-to-install-prometheus-on-ubuntu-16-04

I chose the latest stable build of the exporter from https://prometheus.io/download/#node_exporter

You may need to update the .py file if a new version comes out or you want a different version.

``` useradd --no-create-home --shell /bin/false node_exporter ```

``` wget https://github.com/prometheus/node_exporter/releases/download/v0.16.0/node_exporter-0.16.0.linux-amd64.tar.gz ```

``` sha256sum node_exporter-0.16.0.linux-amd64.tar.gz ```

``` mkdir node_exporter_tmp ```

``` tar xvf node_exporter-0.16.0.linux-amd64.tar.gz```

``` cp node_exporter-0.16.0.linux-amd64/node_exporter /usr/local/bin ```

``` chown node_exporter:node_exporter /usr/local/bin/node_exporter ```

``` rm -rf node_exporter-0.15.1.linux-amd64.tar.gz node_exporter-0.16.0.linux-amd64 ```

``` vi /etc/systemd/system/node_exporter.service```

``` [Unit]
        Description=Node Exporter
        Wants=network-online.target
        After=network-online.target

        [Service]
        User=node_exporter
        Group=node_exporter
        Type=simple
        ExecStart=/usr/local/bin/node_exporter

        [Install]
        WantedBy=multi-user.target 
```

``` systemctl daemon-reload ```

``` systemctl start node_exporter ```

``` systemctl status node_exporter ```

``` systemctl enable node_exporter ```

* sha256 checksum example I used as a start
    * https://gist.github.com/rji/b38c7238128edf53a181
    
    
## How to use this thing

``` sudo su ```

``` git clone https://github.com/tonypnode/prom_node_exporter.git```

``` python3 ./install_exporter.py ```