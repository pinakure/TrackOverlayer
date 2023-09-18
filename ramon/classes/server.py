from classes.endpoints      import Endpoints
from classes.preferences    import Preferences
from classes.log            import Log
from threading              import Thread, Event
from websockets.server      import serve
import json, asyncio,os 

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
    ws      = None

    async def exit():
        import websockets
        async with websockets.connect('ws://localhost:8765') as websocket:
            while 1:
                try:
                    #a = readValues() #read values from a function
                    #insertdata(a) #function to write values to mysql
                    await websocket.send("exit")
                except Exception as e:
                    print(e)

    async def send(message, payload={}):
        from classes.endpoints import response
        if Server.ws is None:
            Log.warning("WEBSOCKET : Attempted to send message to NULL websocket")
            return
        await Server.ws.send( encodeResponse(message, response(payload) ) )


    async def handleRequest(websocket):
        from classes.superchat import Superchat
        Server.ws = websocket
        async for message in websocket:
            if Server.ramon.requesting: return
            if Preferences.settings['debug']: print(f"WS : {message}")
            if message.startswith('exit'                ): os._exit(0)
            elif message.startswith('get-data'          ): await websocket.send( encodeResponse('data'          , Endpoints.getAll()                    ))
            elif message.startswith('get-plugins'       ): await websocket.send( encodeResponse('plugins'       , Endpoints.plugins()                   ))
            elif message.startswith('get-clock'         ): await websocket.send( encodeResponse('clock'         , Endpoints.clock()                     ))
            elif message.startswith('get-game'          ): await websocket.send( encodeResponse('game'          , Endpoints.game()                      ))
            elif message.startswith('get-current-cheevo'): await websocket.send( encodeResponse('current-cheevo', Endpoints.current_cheevo()            ))
            elif message.startswith('get-score'         ): await websocket.send( encodeResponse('score'         , Endpoints.score()                     ))
            elif message.startswith('resize'            ): await websocket.send( encodeResponse('resize'        , Endpoints.resize(message)             ))
            elif message.startswith('move'              ): await websocket.send( encodeResponse('move'          , Endpoints.move(message)               ))
            elif message.startswith('get-recent'        ): await websocket.send( encodeResponse('recent'        , Endpoints.recent()                    ))
            elif message.startswith('get-vpu'           ): await websocket.send( encodeResponse('vpu'           , Endpoints.vpu()                       ))
            elif message.startswith('get-progress'      ): await websocket.send( encodeResponse('progress'      , Endpoints.progress()                  ))
            elif message.startswith('get-superchat'     ): await websocket.send( encodeResponse('superchat'     , Endpoints.superchat()                 ))
            elif message.startswith('mark-superchat'    ): Superchat.mark( message.split( '|' )[1]                                                       )
            elif message.startswith('get-notifications' ): await websocket.send( encodeResponse('notifications' , Server.ramon.data.getNotifications()  ))
            elif message.startswith('mark-notification' ): Server.ramon.data.markNotification( message.split( '|' )[1]                                   )
            else                                         : await websocket.send( encodeResponse('error'         , f'Unknown endpoint "{message}"'       ))

    def thread(main_class):
        asyncio.run(Server.main(main_class))

    def start():
        from classes.ramon import Ramon # private import needed here to avoid import loop
        Server._thread = Thread(target=Server.thread,args=(Ramon,))
        Server._thread.start()

    async def main(main_class):
        Server.ramon = main_class
        Log.info("Starting Live Data Service, listening port 8765")
        async with serve(Server.handleRequest, 'localhost', 8765):
            #while 1:
                print("Websocket Server is Running...")
                await asyncio.Future()