import asyncio
import websockets
import websockets.legacy.server
import func #自定义函数
import sys
import os

url = []
async def recv_user_msg(websocket):
    while True:
        from_html = await websocket.recv()
        # print(from_html)
        if from_html =="connection":  # 这里是难点！在每个通信捂手时发个消息，用一个列表来接受这个用户的身份，离开时一定要remove，因为重新连接时用户名编码会不一样
            url.append(websocket)
        else:
            Freturn = func.GetValue(from_html)
            print(Freturn)
            for item in url:
                await item.send(Freturn)

async def run(websocket, path):
    while True:
        try:
            await recv_user_msg(websocket)
        except websockets.ConnectionClosed:
            url.remove(websocket) #非常重要，如果列表里有冗余对象，middle也会断开连接
            # print("ConnectionClosed...", path)
            # 当没有连接时退出
            if url == []:
                sys.exit()
                print("工具已关闭，再次使用请重启工具！感谢您的使用！")
            break
            

if __name__ == '__main__':
    print("工具加载中，请耐心等待！欢迎使用一陈微信图文排版工具~")
    print("使用过程中请勿关闭此窗口")
    print("—————————————————————————————————————————————————————")
    print("127.0.0.1:10086 websocket...")
    a = os.path.dirname(sys.argv[0])  # 获取软件所在目录
    os.popen(a + "/index.html")
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, "127.0.0.1", 10086))
    asyncio.get_event_loop().run_forever()
