#Kun Cultivation Manual v1.0


from ast import Num
from email.mime.nonmultipart import MIMENonMultipart
import re,os,random,csv,datetime
from os.path import dirname
from tkinter import N
from tkinter.tix import TList
from nonebot.log import logger
from nonebot import on_command
from nonebot.params import State, CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, GROUP, Message, GroupMessageEvent, GroupRequestEvent, MessageEvent
import pandas as pd
import numpy as np

go = on_command("出战",aliases={"分配"},permission=GROUP)
book = on_command("养鲲手册",aliases={"鲲之手册"},permission=GROUP)
fish = on_command("钓鱼",aliases={"fish", "抓鱼", "捕鱼"},permission=GROUP)
self = on_command("我的鲲界",permission=GROUP)
path = dirname(__file__) + "/resources"
path2 = dirname(__file__)
set = on_command("创建xxxx鲲界",permission=GROUP)
add = on_command("新xxxx增",permission=GROUP)
acd = 300
fp = on_command("分配", permission=GROUP, priority=10)
tk = on_command("吞鱼", aliases={"吃鱼"}, permission=GROUP)
cj = on_command("出击", aliases={"战斗"}, permission=GROUP)
#a qq
#b 鱼数
#c cd
#我的鲲
#d 鲲名
#e 经验值
#f 等级
#g 血量
#h 防御
#i 攻击
#j 暴击效果
#k 血气状态

#菜单
@book.handle()
async def _handle(event: GroupMessageEvent):
    await book.send("测试玩法：\n我的鲲界|钓鱼/抓鱼\n吞鱼|分配|出击")

#判断有无该玩家，添加该玩家
@add.handle()
async def _handle(event: GroupMessageEvent):
    gid = event.get_user_id()
    df = pd.read_csv(path2 + "/resc.csv")
    l = df['a'].values.tolist()
    if int(gid) not in l:
        df2 = {'a':int(gid),'b':'0','c':'','d':'','e':'','f':''}
        df = df.append(df2,ignore_index = True)
    df.to_csv(path2 + "/resc.csv", index = False)

#输出玩家鲲界信息
@self.handle()
async def _handle(event: GroupMessageEvent):
    gid = event.get_user_id()
    df = pd.read_csv(path2 + "/resc.csv")
    l = df['a'].values.tolist()
    if int(gid) not in l:
        await self.send("ERROR~您还没有创建鲲界，已经为您创建")
        df2 = {'a':int(gid),'b':'0','c':str(datetime.datetime.now()),'d':'元鲲','e':'','f':'1','g':'0','h':'0','i':'0','j':'0','k':'100'}#如果不存在玩家，新建玩家数据
        df = df.append(df2,ignore_index = True)
        df.to_csv(path2 + "/resc.csv", index = False)
    else:
        await self.send(
          "鲲界\n玩家：" + str(df.a[df.a==int(gid)].values)
        + "\n普通鱼数：" + str(int(df.b[df.a==int(gid)].values)) + "只"
        + "\n鲲名：" + str(df.d[df.a==int(gid)].values)
        + "\n等级(点数)：" + str(int(df.f[df.a==int(gid)].values))
        + "\n血量：" + str(int(df.g[df.a==int(gid)].values)) + "(" + str((int(df.g[df.a==int(gid)].values) + 1 ) * 100) + ")"
        + "\n防御：" + str(int(df.h[df.a==int(gid)].values)) + "(" + str(int(df.h[df.a==int(gid)].values * 5 )) + ")"
        + "\n攻击：" + str(int(df.i[df.a==int(gid)].values)) + "(" + str((int(df.i[df.a==int(gid)].values) + 1 ) * 10 )+ ")"
        + "\n暴击效果：" + str(int(df.j[df.a==int(gid)].values))
        )

#修改玩家指定数值
@set.handle()
async def _handle(event: GroupMessageEvent):
    gid = event.get_user_id()
    df = pd.read_csv(path2 + "/resc.csv")
    #df.b[df.a==int(gid)] = 200
    df.to_csv(path2 + "/resc.csv", index = False)

#钓鱼 获得随机鱼数并存在鲲界
@fish.handle()
async def _handle(event: GroupMessageEvent):
    gid = event.get_user_id()
    df = pd.read_csv(path2 + "/resc.csv")
    l = df['a'].values.tolist()
    if int(gid) not in l:
        df2 = {'a':int(gid),'b':'0','c':str(datetime.datetime.now()),'d':'元鲲','e':'','f':'1','g':'0','h':'0','i':'0','j':'0','k':'100'}#如果不存在玩家，新建玩家数据
        df = df.append(df2,ignore_index = True)
        df.to_csv(path2 + "/resc.csv", index = False)

    cdt = str(df.c[df.a==int(gid)].values).replace("['","")
    cdtt = cdt.replace("']","")
    cd_time = datetime.datetime.strptime(cdtt, "%Y-%m-%d %H:%M:%S.%f")
    now = datetime.datetime.now()

    if int(str((now - cd_time).seconds)) > int(acd):
        df.c[df.a==int(gid)] = datetime.datetime.now()
        fnum = random.randint(0, 100)
        if fnum < 10:
            await fish.send("你才钓了" + str(fnum) + "条鱼，还不够交钓鱼费的！鱼全部没收了！")
        elif fnum == 10:
            await fish.send("你钓的鱼数量刚好交钓鱼费，白忙活了！")
        elif fnum >= 10:
            await fish.send("你钓了" + str(fnum) + "条鱼，扣除10条鱼作为钓鱼费，剩下的鱼都是你的了！")
            df.b[df.a==int(gid)] = fnum - 10 + df.b[df.a==int(gid)]
            df.to_csv(path2 + "/resc.csv", index = False)
    else:
        left = int(acd) - int(str((now - cd_time).seconds))
        await self.send("钓鱼CD中，剩%d秒" % left)

#参数判断
@fp.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg(), state: T_State=State()):
    args = args.extract_plain_text().strip().split()
    # logger.info(args)
    if not args:
        pass
    elif args and len(args) == 1:
        state['fp'] = args[0]
    else:
        await fp.finish('参数错误QAQ')

#点数分配
@fp.got('fp', prompt='请分配点数:\n分配 [血量]-[防御]-[攻击]-[暴击效果]')
async def _handle(bot: Bot, event: GroupMessageEvent, state: T_State=State()):
    gid = event.get_user_id()
    df = pd.read_csv(path2 + "/resc.csv")
    l = df['a'].values.tolist()
    if int(gid) not in l:
        df2 = {'a':int(gid),'b':'0','c':str(datetime.datetime.now()),'d':'元鲲','e':'','f':'1','g':'0','h':'0','i':'0','j':'0','k':'100'}#如果不存在玩家，新建玩家数据
        df = df.append(df2,ignore_index = True)
        df.to_csv(path2 + "/resc.csv", index = False)
    _fp = state['fp']
    if re.match(r'^\d+[-]\d+[-]\d+[-]\d+$', _fp):
        # <x>d<y>
        info = _fp.split('-')
        xl = int(info[0])
        fy = int(info[1])
        gj = int(info[2])
        bj = int(info[3])
        ds = int(df.f[df.a==int(gid)])
    else:
        await fp.finish(f'格式不对呢, 请重新输入: 分配 [血量]-[防御]-[攻击]-[暴击效果]')
    if xl + fy + gj + bj > ds :
        await fp.finish(f'ERROR~点数不足😅')
    df.g[df.a==int(gid)] = xl
    df.h[df.a==int(gid)] = fy
    df.i[df.a==int(gid)] = gj
    df.j[df.a==int(gid)] = bj
    df.to_csv(path2 + "/resc.csv", index = False)
    await self.send("分配成功，输入‘我的鲲界’查看分配情况")
        
#吞鲲
@tk.handle()
async def _handle( event: GroupMessageEvent):
    gid = event.get_user_id()
    df = pd.read_csv(path2 + "/resc.csv")
    l = df['a'].values.tolist()
    if int(gid) not in l:
        df2 = {'a':int(gid),'b':'0','c':str(datetime.datetime.now()),'d':'元鲲','e':'','f':'1','g':'0','h':'0','i':'0','j':'0','k':'100'}#如果不存在玩家，新建玩家数据
        df = df.append(df2,ignore_index = True)
        df.to_csv(path2 + "/resc.csv", index = False)
    if int(df.b[df.a==int(gid)].values) == 0:
        await self.send("你还没有鱼呢，快去钓鱼吧！")
    elif int(df.b[df.a==int(gid)].values) < 50:
        await self.send("你喂的鱼太少了！你的鲲每次吃50只才能填饱肚子！")
    elif int(df.b[df.a==int(gid)].values) >= 50:
        df.b[df.a==int(gid)] = df.b[df.a==int(gid)] - 50
        df.f[df.a==int(gid)] = df.f[df.a==int(gid)] + 1
        df.to_csv(path2 + "/resc.csv", index = False)
        await self.send("食饱鲲升级！")


@cj.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg(), state: T_State=State()):
    args = args.extract_plain_text().strip().split()
    # logger.info(args)
    if not args:
        pass
    elif args and len(args) == 1:
        state['cj'] = args[0]
    else:
        await cj.finish('参数错误QAQ')
#战斗系统
@cj.got('cj',prompt='请出击玩家：出击 [QQ]')
async def _handle(bot: Bot, event: GroupMessageEvent, state: T_State=State()):
    gid = event.get_user_id()
    df = pd.read_csv(path2 + "/resc.csv")
    l = df['a'].values.tolist()
    if int(gid) not in l:
        await cj.finish(f'新来的？先去钓鱼吧😅') 
    else:
        _cj = state['cj']
        print (str(_cj))
        print (int(_cj))
    if int(_cj) not in l:
        await cj.finish(f'ERROR~😅\n请精准出击:\n出击 [QQ]') 
    xl1 = int(df.g[df.a==int(gid)])
    xl2 = int(df.g[df.a==int(_cj)])
    fy1 = int(df.h[df.a==int(gid)])
    fy2 = int(df.h[df.a==int(_cj)])
    gj1 = int(df.i[df.a==int(gid)])
    gj2 = int(df.i[df.a==int(_cj)])
    bj1 = int(df.j[df.a==int(gid)])
    bj2 = int(df.j[df.a==int(_cj)])
    x1 = (xl1 + 1) * 100
    x2 = (xl2 + 1) * 100
    hh = 0
    bjcs1 = 0
    bjcs2 = 0
    while x1 > 0 and x2 > 0:
        bjinfo1 = 0
        bjinfo2 = 0
        bjl1 = random.randint(0, 100)
        bjl2 = random.randint(0, 100)
        if bjl1 <=30:
            bjinfo1 = 1
        if bjl2 <=30:
            bjinfo2 = 1
        sh1 = (gj1 + 1) * 10 + (bj1 + gj1) * 10 * bjinfo1 - fy2 * 5 
        sh2 = (gj2 + 1) * 10 + (bj2 + gj1) * 10 * bjinfo2 - fy1 * 5
        if sh1 > 10 :
            x2 = x2 - sh1
        else:
            x2 = x2 - 10
        if sh2 > 10 :
            x1 = x1 - sh2
        else:
            x1 = x1 - 10
        hh = hh + 1
        bjcs1 = bjcs1 + bjinfo1
        bjcs2 = bjcs2 + bjinfo2
    if x1 - x2 > 0:
        await cj.finish(f'恭喜出击方获得胜利\n本次对决持续了' + str(hh) + '回合\n出击方共暴击'+str(bjcs1)+'次\n防守方共暴击'+str(bjcs2)+'次') 
    if x1 - x2 < 0:
        await cj.finish(f'恭喜防守方守擂成功\n本次对决持续了' + str(hh) + '回合\n出击方共暴击'+str(bjcs1)+'次\n防守方共暴击'+str(bjcs2)+'次') 
    if x1 - x2 == 0:
        await cj.finish(f'双方难分伯仲，最后都英勇倒下😅\n本次对决持续了' + str(hh) + '回合\n出击方共暴击'+str(bjcs1)+'次\n防守方共暴击'+str(bjcs2)+'次') 
