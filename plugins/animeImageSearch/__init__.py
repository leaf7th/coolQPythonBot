from nonebot import (CommandSession, IntentCommand, on_command,
                     on_natural_language)

from .animeSearchAPI import searchAnimeByScreenshot
from .config import *
from .imageCache import downloadImage


@on_command('anime_screenshot_search', aliases=('以图搜番', '搜番', '以图识番'))
async def animeSearch(session: CommandSession):
    imageResource = session.get('image', prompt='请将图片和搜番指令一同发送')
    result = await searchAnimeByScreenshot(imageResource)
    if result.get('error'):
        await session.send('图片搜索失败,错误码%d' % result['error'])
    else:
        resultList = []
        for perDoc in result['docs']:
            result = REPLY_FORMAT.format(**perDoc)
            resultList.append(result)
        if resultList:
            returnResult = ''.join(resultList[:RETURN_INFO_SIZE])
        else:
            returnResult = '没有找到相关番剧'
        await session.send(returnResult, at_sender=True)


@on_natural_language(keywords=('以图搜番', '以图识番'))
async def _(session):
    return IntentCommand(90.0, 'anime_screenshot_search')


@animeSearch.args_parser
async def _(session: CommandSession):
    for perKeyword in END_SYMBOL:
        if perKeyword in session.current_arg_text:
            session.finish('指令提前结束,感谢您的使用!')
    if session.current_arg_images:
        imgUrl = session.current_arg_images[0]
        imgBase64, imgSize = await downloadImage(imgUrl)
    else:
        session.pause('请发送一张图片来进行搜索')
    if imgSize >= 1024**2:
        session.pause('图片大小超过限制!必须小于1MB,您的图片为%.3fMB' % imgSize / 1024**2)
    session.state['image'] = imgBase64
    return
