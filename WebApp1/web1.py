import sys
import aiohttp_jinja2
import jinja2
from aiohttp import web

from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack 
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

import socketio

from routes import setup_routes

ROOT = '/home/pi/RescueOnTheWheelsProject/WebApp/website'

socket = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
socket.attach(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))
setup_routes(app)
    

@socket.on('t')
async def test(sid, test):
    print(test)

async def offer(request):
    
    params = await request.json()
    offer = RTCSessionDescription(
        sdp=params['sdp'],
        type=params['type'])

    pc = RTCPeerConnection()
    pcs.add(pc)

    # prepare local media
    
    player = MediaPlayer(os.path.join(ROOT, 'demo-instruct.wav'))
    recorder = MediaRecorder("test")
    

    @pc.on('iceconnectionstatechange')
    async def on_iceconnectionstatechange():
        print('ICE connection state is %s' % pc.iceConnectionState)
        if pc.iceConnectionState == 'failed':
            await pc.close()
            pcs.discard(pc)

    @pc.on('track')
    def on_track(track):
        print('Track %s received' % track.kind)

        pc.addTrack(player.audio)
        recorder.addTrack(track)

        @track.on('ended')
        async def on_ended():
            print('Track %s ended' % track.kind)
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type='application/json',
        text=json.dumps({
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type
        }))

pcs = set()

async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


def main(argv):
    
    web.run_app(app, host='192.168.137.19', port=argv[0])

if __name__ == '__main__':
    main(sys.argv[1:])
