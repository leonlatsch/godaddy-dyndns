# godaddy-dyndns

Python based GoDaddy dyndns script using only the GoDaddy api.

## Functionallity

- Gets the public ip using [api.ipify.org](https://api.ipify.org/?format=raw). Fallback: [ip.42.pl](http://ip.42.pl/raw)
- Caches the last obtained ip and checks for a change.
- Creates or updates the dns entry with the name of `@` and the type of `A` pointing to your ip in case of a new ip.
- **Won't work if there are more than one entries matching this condition!** (very unlikely)

## Usage

- Clone the repository.
- Enter your api credentials and domain name into `godaddy-dyndns.conf`. **You can create api credentials [here](https://developer.godaddy.com).**
- run the script to test it (You may have to add execution permissions).
- I recommend setting up a cron job to run the script every hour: `0 * * * * /path/to/script.py`. **[Help](https://crontab.guru)**

If you have questions feel free to create an issue.
