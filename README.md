# godaddy-dyndns

Python based GoDaddy dyndns script using only the GoDaddy api.

## Functionallity

- Gets the public ip using [ip.42.pl](http://ip.42.pl/raw). Fallback: [api.ipify.org](https://api.ipify.org/?format=raw)
- Creates or updates the dns entry with the name of `@` and the type of `A`.
- **Won't work if there are more than one entries matching this condition!** (very unlikely)

## Usage

- Clone the repository.
- Enter your api credentials and domain name at the top of the script.
- run the script to test it.
- I reccomand setting up a cron job to update the dns entry every hour: `0 * * * * /path/to/script.py`

If you have questions feel free to create an issue.
