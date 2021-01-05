import sys
from typing import Coroutine, Optional, Union, List

from .kwargs import build_kwargs
from .models import Devices, Device, Maintainers, Maintainer, OEMs, Releases, Release, Updates
from .sync import OrangeFoxAPI
from .types import ReleaseType, DevicesSort, MaintainersSort, ReleasesSort
from .version import version

HEADERS = {
    'User-Agent': 'OrangeFoxAPI-pylib',
    'Lib-Version': version + '-async',
    'Python-version': str(sys.hexversion)
}


# noinspection DuplicatedCode
class OrangeFoxAsyncAPI(OrangeFoxAPI):
    cache_class: Optional[Coroutine]

    def __init__(self, cache_class: Optional[Coroutine] = None, **kwargs):
        super().__init__(**kwargs)

        self.cache_class = cache_class

        import aiohttp
        self.session = aiohttp.ClientSession(headers=HEADERS)

    async def _send_request(self, api_method: str) -> Union[str, None]:
        url = self.host + api_method

        async with self.session.get(url) as r:
            if r.status == 200:
                return await r.text()
            elif r.status == 402:
                raise TypeError('Validation error')
            elif r.status == 404:
                return None
            else:
                raise ValueError(f"{r.status}: {r.text}")

    async def _cached_request(self, api_method: str) -> Union[dict, None]:
        if not self.cache_class:
            return self._decode_request(await self._send_request(api_method))

        if cached := (await self.cache_class.get(api_method)):
            return self._decode_request(cached)

        data = await self._send_request(api_method)
        await self.cache_class.set(api_method, data)
        await self.cache_class.expire(api_method, self.cache_expire)

        return self._decode_request(cached)

    def close(self):
        if self.session is not None:
            return self.session.close()

    # Devices

    async def devices(
            self,
            id: Optional[Union[List[str], str]] = None,
            oem_name: Optional[Union[List[str], str]] = None,
            codename: Optional[Union[List[str], str]] = None,
            model_name: Optional[Union[List[str], str]] = None,
            supported: Optional[Union[List[bool], bool]] = None,
            maintainer_id: Optional[Union[List[str], bool]] = None,
            release_type: Optional[ReleaseType] = None,
            skip: Optional[int] = None,
            sort: Optional[DevicesSort] = None,
            limit: Optional[int] = None

    ) -> Devices:
        kwargs = build_kwargs({
            'id': id,
            'oem_name': oem_name,
            'codename': codename,
            'model_name': model_name,
            'supported': supported,
            'maintainer_id': maintainer_id,
            'release_type': release_type,
            'sort': sort,
            'skip': skip,
            'limit': limit
        })

        if not (data := await self._cached_request(self._url_encode('/devices/', **kwargs))):
            return Devices(data=[], count=0)
        return Devices(**data)

    async def device(
            self,
            id: Optional[str] = None,
            codename: Optional[str] = None
    ) -> Union[Device, None]:
        kwargs = build_kwargs({
            'id': id,
            'codename': codename
        })

        if not (data := await self._cached_request(self._url_encode('/devices/get/', **kwargs))):
            return None

        return Device(**data)

    # OEMs

    async def oems(self) -> OEMs:
        if not (data := await self._cached_request(self._url_encode('/oems/'))):
            return OEMs(data=[], count=0)
        return OEMs(**data)

    # Maintainers

    async def maintainers(
            self,
            id: Optional[Union[List[str], str]] = None,
            name: Optional[Union[List[str], str]] = None,
            username: Optional[Union[List[str], str]] = None,
            sort: Optional[MaintainersSort] = None,
            skip: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Maintainers:
        kwargs = build_kwargs({
            'id': id,
            'sort': sort,
            'name': name,
            'username': username,
            'skip': skip,
            'limit': limit
        })

        if not (data := await self._cached_request(self._url_encode('/users/maintainers/', **kwargs))):
            return Maintainers(data=[], count=0)
        return Maintainers(**data)

    async def maintainer(
            self,
            id: Optional[str] = None,
            username: Optional[str] = None,
    ) -> Union[Maintainer, None]:
        kwargs = build_kwargs({
            'id': id,
            'username': username
        })
        if not (data := await self._cached_request(self._url_encode('/users/maintainers/get/', **kwargs))):
            return None
        return Maintainer(**data)

    # Releases

    async def releases(self,
                       id: Optional[Union[List[str], str]] = None,
                       device_id: Optional[Union[List[str], str]] = None,
                       codename: Optional[Union[List[str], str]] = None,
                       version: Optional[Union[List[str], str]] = None,
                       type: Optional[ReleaseType] = None,
                       filename: Optional[Union[List[str], str]] = None,
                       skip: Optional[int] = None,
                       sort: Optional[ReleasesSort] = None,
                       limit: Optional[int] = None
                       ) -> Releases:
        kwargs = build_kwargs({
            'id': id,
            'device_id': device_id,
            'codename': codename,
            'version': version,
            'type': type,
            'filename': filename,
            'sort': sort,
            'skip': skip,
            'limit': limit
        })
        if not (data := await self._cached_request(self._url_encode('/releases/', **kwargs))):
            return Releases(data=[], count=0)
        return Releases(**data)

    async def release(self,
                      id: Optional[Union[List[str], str]] = None,
                      filename: Optional[Union[List[str], str]] = None,
                      ) -> Union[Release, None]:
        kwargs = build_kwargs({
            'id': id,
            'filename': filename
        })
        if not (data := await self._cached_request(self._url_encode('/releases/get/', **kwargs))):
            return None
        return Release(**data)

    async def updates(self,
                      last_known_id: str,
                      device_id: Optional[Union[List[str], str]] = None,
                      release_type: Optional[Union[List[str], str]] = None,
                      skip: Optional[int] = None,
                      limit: Optional[int] = None
                      ) -> Updates:

        kwargs = build_kwargs({
            'device_id': device_id,
            'release_type': release_type,
            'skip': skip,
            'limit': limit
        })

        if not (data := await self._cached_request(self._url_encode(f'/updates/{last_known_id}/', **kwargs))):
            return Updates(data=[], count=0)
        return Updates(**data)
