# godaddy-dyndns

![python-version](https://img.shields.io/badge/python-3.7-blue)
![GitHub](https://img.shields.io/github/license/leonlatsch/godaddy-dyndns)
![Maintenance](https://img.shields.io/maintenance/yes/2019)


Python based GoDaddy dyndns script using only the GoDaddy api.

## Functionallity

- Gets the public ip using [api.ipify.org](https://api.ipify.org/?format=raw). Fallback: [ip.42.pl](http://ip.42.pl/raw)
- Caches the last obtained ip and checks for a change.
- If it has changed, it creates or updates the `A` record entry for the configured host with the new ip.
- **Won't work if there are more than one entries matching this condition!** (very unlikely)

## Usage

- Clone the repository.
- Enter your api credentials and domain name into `godaddy-dyndns.conf`. **You can create api credentials [here](https://developer.godaddy.com).**
- run the script to test it (You may have to add execution permissions).
- I recommend setting up a cron job to run the script every hour: `0 * * * * /path/to/script.py`. **[Help](https://crontab.guru)**

If you have questions feel free to create an issue.

## Docker / in dev
Run godaddy-dyndns as docker container like this:
```
docker volume create godaddy-dyndns-data
docker run -d -v godaddy-dyndns-data:/config leonlatsch/godaddy-dyndns
```

`godaddy-dyndns.conf` is located in the new volume.