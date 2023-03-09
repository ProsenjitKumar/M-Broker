import asyncio
import geoip2.webservice


async def main():
    async with geoip2.webservice.AsyncClient(42, 'license_key') as client:
        response = await client.city('203.0.113.0')
        print(response.country.iso_code)
        print(response.country.name)