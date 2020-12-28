from orangefoxapi import OrangeFoxAPI

api = OrangeFoxAPI()


def get_devices_ids():
    devices = api.devices(oem_name='Xiaomi')
    for device in devices:
        print(device.id)


def get_latest_release():
    latest_release = (api.releases(limit=1)).data[0]
    release = api.release(id=latest_release.id)
    print(release)


get_devices_ids()
get_latest_release()
