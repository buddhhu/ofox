# Copyright (C) 2017-2020 OrangeFox Recovery
#
# This file is part of oBOT.
#
# oBOT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

import aiohttp

from typing import Union


class OrangeFoxAPI:
    def __init__(
            self,
            host='https://api.orangefox.download/v2/',
            ssl=True,
            cache=None,
            cache_expire=300,
            json=None
    ):
        self.host = host
        self.ssl = ssl
        self.cache = cache
        self.cache_expire = cache_expire

        if json:
            self.json = json
        else:
            import json
            self.json = json

    async def _send_request(self, api_method: str) -> Union[str, None]:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=self.ssl)) as session:
            async with session.get(self.host + api_method) as response:
                if response.status == 404:
                    return None

                text = await response.text()
                return text

    async def _cached_or_make_request(self, api_method: str) -> Union[list, dict]:
        if self.cache:
            if cached := await self.cache.get(api_method):
                return self.json.loads(cached)

        data = await self._send_request(api_method)

        if self.cache:
            await self.cache.set(api_method, data)
            await self.cache.expire(api_method, self.cache_expire)

        if data == 404:
            return None

        return self.json.loads(data)

    async def ping(self) -> bool:
        """
        This method will return True in case if OrangeFox API is alive.
        Warning! This method is uncached!
        :return: bool
        """
        data = await self._send_request('/ping')
        if data == 'PONG':
            return True

        return False

    async def list_oems(self) -> list:
        return await self._cached_or_make_request('/oem')

    async def get_oem(self, oem: str, only_codenames=False) -> list:
        return await self._cached_or_make_request(f'/oem/{oem}?{only_codenames=}')

    async def list_devices(self, only_codenames=False) -> list:
        return await self._cached_or_make_request(f'/device?{only_codenames=}')

    async def get_device(self, codename: str) -> dict:
        return await self._cached_or_make_request(f'/device/{codename}')

    async def get_devices_with_releases(self, release_type=None) -> dict:
        return await self._cached_or_make_request(f"/device/releases/{release_type or 'any'}")

    async def get_oem_devices_with_releases(self, oem_name, release_type=None) -> dict:
        return await self._cached_or_make_request(f"/oem/{oem_name}/releases/{release_type or 'any'}")

    async def get_release(self, release_id: str) -> dict:
        return await self._cached_or_make_request(f'/releases/{release_id}')

    async def get_last_release(self, release_type=None) -> dict:
        return await self._cached_or_make_request(f"/releases/{release_type or 'any'}/last")

    async def get_device_release(self, codename: str, release_type=None, version=None) -> dict:
        method = f"/device/{codename}/releases/{release_type or 'any'}"
        if version:
            method += f'/{version}'

        return await self._cached_or_make_request(method)

    async def get_updates(self, var: Union[str, int]) -> list:
        return await self._cached_or_make_request(f'/releases/updates/{var}')

    async def get_device_updates(self, codename: str, var: Union[str, int], build_type=None) -> list:
        return await self._cached_or_make_request(f"/device/{codename}/releases/{build_type or 'any'}/updates/{var}")
