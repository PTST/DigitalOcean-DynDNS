# DigitalOcean-DynDNS
![ci](https://github.com/PTST/DigitalOcean-DynDNS/workflows/ci/badge.svg?branch=master)
## Usage

Here are some example snippets to help you get started creating a container.

### docker

```
docker create \
  --name=digitalocean-dyndns \
  -e DO_TOKEN=<API_KEY> \
  -e BASE_URL=<DOMAIN> \
  -e HOST_NAME=<SUBDOMAIN> \
  -e UPDATE_INTERVAL=300 \
  --restart unless-stopped \
  ptst/digitalocean-dyndns
```

### docker-compose

Compatible with docker-compose v2 schemas.

```
version: "3"
services:
  digitalocean-dyndns:
    container_name: digitalocean-dyndns
    environment:
        - DO_TOKEN=<API_KEY>
        - BASE_URL=<DOMAIN>
        - HOST_NAME=<SUBDOMAIN>
        - UPDATE_INTERVAL=300
    image: ptst/digitalocean-dyndns
    restart: unless-stopped
```

## Parameters

Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 8080:80` would expose port `80` from inside the container to be accessible from the host's IP on port `8080` outside the container.

| Parameter | Function |
| :----: | --- |
| `-e DO_TOKEN=<API_KEY>` | Your DigitalOcean API key |
| `-e BASE_URL=<DOMAIN>` | The base of the domain name you want to update |
| `-e HOST_NAME=<SUBDOMAIN>` | The subdomain you want to update, set to @ for no subdomain |
| `-e UPDATE_INTERVAL=300` | How often should the process check for IP updates |
