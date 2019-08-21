import requests
from utils.exception import BotProgramError
from utils.customDecorators import CatchRequestsException
from .config import Config


@CatchRequestsException(prompt='下载用户发出图片失败')
def imageDownload(url: str):
    data = requests.get(url, timeout=3)
    data.raise_for_status()
    dataBytes = data.content
    return dataBytes, len(dataBytes)


@CatchRequestsException(prompt='上传文件出错', retries=Config.api.retries)
def whatanimeUpload(file: str) -> dict:
    if len(file) >= 1024**2:
        raise BotProgramError('您发送的图片大小超过限制')
    params = {
        'url':
        Config.api.address,
        'headers': {
            'Content-Type': 'application/json'
        },
        'json': {
            'image': file
        },
        'timeout': (3, None),
        'proxies': ({
            'http': Config.proxy.address,
            'https': Config.proxy.address
        } if Config.proxy.enable else {})
    }
    data = requests.post(**params)
    data.raise_for_status()
    return data.json()