from pathlib import Path

import nonebot
from nonebot import get_driver
import sqlite3
import nonebot,re
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent
from pathlib import Path

from nonebot import get_driver,on_message,on_command
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.rule import to_me
from pathlib import Path
from typing import Union
from nonebot.adapters import Bot

from .config import Config
from .chat_core import chatGPT_class,chatGPT_chat,chatGPT_search

import requests

loopCount = 0

global_config = get_driver().config
config = Config.parse_obj(global_config)

gpthelp_kokoro = on_command("gpthelp_kokoro", aliases={"gpt帮助"}, priority=80, block=True) # 帮助

findsessions_kokoro = on_command("findsessions_kokoro",rule=to_me(), aliases={"对话列表"}, priority=90, block=True) # 查找所有和此用户有关的对话
sessionDetail_kokoro = on_command("sessionDetail_kokoro",rule=to_me(), aliases={"查看对话"}, priority=91, block=True) # 查看特定对话

successSession_kokoro = on_command("successSession_kokoro",rule=to_me(), aliases={"继承对话"}, priority=92, block=True) # 继承特定的对话
usePerset_kokoro = on_command("usePerset_kokoro",rule=to_me(), aliases={"使用预设"}, priority=93, block=True) # 使用特定的预设
setPerset_kokoro = on_command("setPerset_kokoro",rule=to_me(), aliases={"生成预设"}, priority=94, block=True) # 将对话设置为预设
preset_list_kokoro = on_command("preset_list_kokoro",rule=to_me(), aliases={"预设列表"}, priority=89, block=True) # 查看所有预设

noPerset_kokoro = on_command("noPerset_kokoro",rule=to_me(), aliases={"纯净模式"}, priority=80, block=True) # 不使用预设

closeSession_kokoro = on_command("closeSession_kokoro",rule=to_me(), aliases={"结束对话"}, priority=99, block=True) # 结束对话

chatgpt_kokoro = on_command("chatgpt_kokoro",rule=to_me(), aliases={""}, priority=100) # 正常对话

@chatgpt_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, chatgpt_kokoro: chatgpt_kokoro):

    '''平常聊天指令'''

    # msg_json = {}
    # msg_json['post_type'] = event.post_type
    # msg_json['sub_type'] = event.sub_type
    # msg_json['user_id'] = event.user_id
    # msg_json['message_type'] = event.message_type
    # msg_json['message_id'] = event.message_id
    # msg_json['message'] = str(event.message)
    # msg_json['original_message'] = event.original_message
    # msg_json['raw_message'] = event.raw_message
    # msg_json['to_me'] = event.to_me
    #
    # sender_json = {}
    # sender_json['nickname'] = event.sender.nickname
    # sender_json['sex'] = event.sender.sex
    # sender_json['age'] = event.sender.age
    # sender_json['card'] = event.sender.card
    # sender_json['role'] = event.sender.role
    # sender_json['user_id'] = event.sender.user_id
    # sender_json['title'] = event.sender.title
    # Bot_qq = bot.self_id
    #
    # await chatgpt_kokoro.send(str(msg_json))
    # await chatgpt_kokoro.send(str(Bot_qq))
    # await chatgpt_kokoro.finish(str(sender_json))

    gptobject = chatGPT_chat(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=chatgpt_kokoro)

    res = await gptobject.chatCore()

    if len(str(res)) < 50:
        await chatgpt_kokoro.finish(str(res), at_sender=True)

    elif  len(str(res)) >= 50:
        resjson = [
            {
                "type": "node",
                "data": {
                    "name": "可可萝",
                    "uin": bot.self_id,
                    "content": str(res)
                }
            }
        ]


        if event.message_type == 'private':
            await bot.call_api("send_private_forward_msg", user_id=event.user_id, messages=resjson)

        elif event.message_type == 'group':
            await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=resjson)

@closeSession_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, closeSession_kokoro: closeSession_kokoro):

    '''结束会话指令'''

    gptobject = chatGPT_chat(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=chatgpt_kokoro)

    res = await gptobject.closeSession()

    await closeSession_kokoro.finish(str(res), at_sender=True)

'''session related'''

@sessionDetail_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, sessionDetail_kokoro: sessionDetail_kokoro):

    '''查看会话详情指令'''

    msg = str(event.message)

    sessionID = re.sub('查看对话','',msg)
    sessionID = sessionID.strip()

    gptobject = chatGPT_search(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=chatgpt_kokoro,sessionID=sessionID)

    await gptobject.getDetails()

    # await sessionDetail_kokoro.finish(str(res), at_sender=True)

@findsessions_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, findsessions_kokoro: findsessions_kokoro):

    '''查看会话列表'''

    gptobject = chatGPT_search(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=chatgpt_kokoro)

    await gptobject.getList()

    # await findsessions_kokoro.finish(str(res), at_sender=True)

@successSession_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, successSession_kokoro: successSession_kokoro):

    '''查看会话详情指令'''

    msg = str(event.message)

    sessionID = re.sub('继承对话','',msg)
    sessionID = sessionID.strip()

    gptobject = chatGPT_chat(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=chatgpt_kokoro,sessionID=sessionID)

    res = await gptobject.successSession()

    await successSession_kokoro.finish(str(res), at_sender=True)

'''preset related'''

@usePerset_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, usePerset_kokoro: usePerset_kokoro):

    '''使用预设'''

    msg = str(event.message)

    presetName = re.sub('使用预设','',msg)
    presetName = presetName.strip()

    gptobject = chatGPT_chat(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=chatgpt_kokoro)

    res = await gptobject.usePreset(presetName=presetName)

    await usePerset_kokoro.finish(str(res), at_sender=True)

@noPerset_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, noPerset_kokoro: noPerset_kokoro):

    '''不使用预设开启新的聊天'''

    gptobject = chatGPT_chat(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=noPerset_kokoro)

    res = await gptobject.pureMode()

    if len(str(res)) < 50:
        await noPerset_kokoro.finish(str(res), at_sender=True)

    elif  len(str(res)) >= 50:
        resjson = [
            {
                "type": "node",
                "data": {
                    "name": "可可萝",
                    "uin": bot.self_id,
                    "content": str(res)
                }
            }
        ]


        if event.message_type == 'private':
            await bot.call_api("send_private_forward_msg", user_id=event.user_id, messages=resjson)

        elif event.message_type == 'group':
            await bot.call_api("send_group_forward_msg", group_id=event.group_id, messages=resjson)

@setPerset_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, setPerset_kokoro: setPerset_kokoro):

    '''拿到sessionID和预设名称 设置预设'''

    msg = str(event.message)

    res = re.sub('生成预设','',msg)
    res = res.strip()
    reslist = re.split(' ',res)

    if len(reslist) != 2:
        setPerset_kokoro.finish('请输入正确的格式：生成预设 sessionID 新预设名称', at_sender=True)

    sessionID = reslist[0]
    presetName = reslist[1]


    gptobject = chatGPT_chat(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=chatgpt_kokoro)

    res = await gptobject.generatePreset(sessionID=sessionID,presetName=presetName)

    await setPerset_kokoro.finish(str(res), at_sender=True)

@preset_list_kokoro.handle()
async def handle_func(event: Union[GroupMessageEvent, PrivateMessageEvent], bot: Bot, preset_list_kokoro: preset_list_kokoro):

    '''查看预设列表'''

    gptobject = chatGPT_search(event=event, bot=bot,groupchatmode=False,chatgpt_kokoro=chatgpt_kokoro)

    await gptobject.getpresetList()

    # await preset_list_kokoro.finish(str(res), at_sender=True)

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").
    resolve()))

