from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class GitLabRepo(BaseModel):
    id: int
    name: str
    url: HttpUrl


class DeviceSources(BaseModel):
    device_tree: Optional[GitLabRepo]
    kernel_tree: Optional[GitLabRepo]


class ShortDevice(BaseModel):
    id: str
    codename: str
    oem_name: str
    model_name: str
    full_name: str
    supported: bool

    class Config:
        fields = {'id': '_id'}


class ShortMaintainer(BaseModel):
    id: str
    name: str
    username: str

    class Config:
        fields = {'id': '_id'}


class Device(ShortDevice):
    maintainer: ShortMaintainer
    ab_device: bool
    notes: Optional[str]


class Devices(BaseModel):
    data: List[ShortDevice]
    count: int

    def __iter__(self):
        return self.data.__iter__()


class Telegram(BaseModel):
    id: int
    username: Optional[str]
    url: Optional[HttpUrl]


class GitLab(BaseModel):
    id: int


class Maintainer(ShortMaintainer):
    telegram: Optional[Telegram]
    gitlab: Optional[GitLab]


class Maintainers(BaseModel):
    data: List[ShortMaintainer]
    count: int

    def __iter__(self):
        return self.data.__iter__()


class OEMs(BaseModel):
    data: List[str]
    count: int

    def __iter__(self):
        return self.data.__iter__()


class RecoveryImg(BaseModel):
    size: int
    md5: str


class ShortRelease(BaseModel):
    id: str
    device_id: str
    date: int
    size: int
    md5: str
    version: str
    type: str

    # filename: str

    class Config:
        fields = {'id': '_id'}


class Release(ShortRelease):
    recovery_img: RecoveryImg
    changelog: tuple
    bugs: Optional[tuple]
    notes: Optional[str]
    mirrors: dict


class Releases(BaseModel):
    data: List[ShortRelease]
    count: int

    def __iter__(self):
        return self.data.__iter__()


class Updates(BaseModel):
    data: List[ShortRelease]
    count: int

    def __iter__(self):
        return self.data.__iter__()
