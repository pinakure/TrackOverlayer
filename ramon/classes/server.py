from classes.endpoints import Endpoints
from threading              import Thread
from websockets.server      import serve
import json, asyncio

def encodeResponse(response_type, payload):
    return '{'+f''' "response":"{response_type}","data":{ json.dumps(payload) }'''+"}"

class Server:
    '''
    Overlay server class 
    Listens for messages coming from plugins and 
    Serves fresh data when (and only when) requested
    This class uses a web socket needing port forwarding
    only if overlay is in a remote network, if working in
    localhost no forwarding is needed.
    The class serves as router for the endpoints class 
    '''
    _thread = None
    ramon   = None

    async def handleRequest(websocket):
        async for message in websocket:
            if Server.ramon.requesting: return
            print(f"WS : {message}")
            if   message=='get-data'                    : await websocket.send( encodeResponse('data'           ,  Endpoints.getAll()                   ))
            elif message.startswith('get-plugins')      : await websocket.send( encodeResponse('plugins'        ,  Endpoints.plugins()                  ))
            elif message.startswith('get-game')         : await websocket.send( encodeResponse('game'           ,  Endpoints.game()                     ))
            elif message.startswith('get-score')        : await websocket.send( encodeResponse('score'          ,  Endpoints.score()                    ))
            elif message.startswith('get-recent')       : await websocket.send( encodeResponse('recent'         ,  Endpoints.recent()                   ))
            elif message.startswith('get-notifications'): await websocket.send( encodeResponse('notifications'  ,  Server.ramon.data.getNotifications() ))
            elif message.startswith('get-progress')     : await websocket.send( encodeResponse('progress'       ,  Endpoints.progress()                 ))
            elif message.startswith('mark-notification'): Server.ramon.data.markNotification(message.split('|')[1])
            else:await websocket.send(encodeResponse('error', f'Unknown endpoint "{message}"'))

    def thread(main_class):
        asyncio.run(Server.main(main_class))

    def start():
        from classes.ramon import Ramon # private import needed here to avoid import loop
        Server._thread = Thread(target=Server.thread,args=(Ramon,))
        Server._thread.start()

    async def main(main_class):
        Server.ramon = main_class
        print("Starting Live Data Service, listening port 8765")
        async with serve(Server.handleRequest, 'localhost', 8765):
            while Server.ramon.run:
                await asyncio.Future()