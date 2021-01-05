import asyncio

from orangefoxapi import OrangeFoxAsyncAPI
from orangefoxapi.types import ReleaseType

api = OrangeFoxAsyncAPI()


async def get_devices_ids():
    devices = await api.devices(oem_name='Xiaomi')
    for device in devices:
        print(device.id)


async def get_latest_release():
    latest_release = (await api.releases(limit=1, type=ReleaseType.stable)).data[0]
    release = await api.release(id=latest_release.id)
    print(release)


loop = asyncio.get_event_loop()
loop.run_until_complete(get_devices_ids())
loop.run_until_complete(get_latest_release())
loop.run_until_complete(api.close())
loop.close()
