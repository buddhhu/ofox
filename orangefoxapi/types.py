from enum import Enum


class ReleaseType(Enum):
    stable = 'stable'
    beta = 'beta'


class DevicesSort(Enum):
    device_name_asc = 'device_name_asc'
    device_name_desc = 'device_name_desc'
    codename_asc = 'codename_asc'
    codename_desc = 'codename_desc'
    date_asc = 'date_asc'
    date_desc = 'date_desc'


class MaintainersSort(Enum):
    name_asc = 'name_asc'
    name_desc = 'name_desc'
    nickname_asc = 'nickname_asc'
    nickname_desc = 'nickname_desc'
    date_asc = 'date_asc'
    date_desc = 'date_desc'


class ReleasesSort(Enum):
    size_asc = 'size_asc'
    size_desc = 'size_desc'
    filename_asc = 'filename_asc'
    filename_desc = 'filename_desc'
    date_asc = 'date_asc'
    date_desc = 'date_desc'
