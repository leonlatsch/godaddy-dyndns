# godaddy-dyndns

Python based GoDaddy dyndns script using only the GoDaddy api.

## Functionallity

- Gets the public ip using [api.ipify.org](https://api.ipify.org/?format=raw). Fallback: [ip.42.pl](http://ip.42.pl/raw)
- Creates or updates the dns entry with the name of `@` and the type of `A` pointing to your ip.
- **Won't work if there are more than one entries matching this condition!** (very unlikely)

## Usage

- Clone the repository.
- Enter your api credentials and domain name into `godaddy-dyndns.conf`. __You can create api credentials [here](https://developer.godaddy.com).__
- run the script to test it (You may have to add execution permissions).
- I reccomand setting up a cron job to update the dns entry every hour: `0 * * * * /path/to/script.py`

If you have questions feel free to create an issue.
