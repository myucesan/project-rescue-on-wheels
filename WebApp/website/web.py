import aiohttp_jinja2
import jinja2
import asyncio
import json
import sys
import os

import cv2
from aiohttp import web
from av import VideoFrame

from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

import socketio

from routes import setup_routes

ROOT = '/home/pi/RescueOnTheWheelsProject/WebApp/website'

socket = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
socket.attach(app)
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader('./templates'))


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
    recorder = MediaRecorder("test.wav")

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


if __name__ == '__main__':
    app.on_shutdown.append(on_shutdown)
    app.router.add_post('/offer', offer)
    setup_routes(app)
    web.run_app(app, host='192.168.137.19', port=sys.argv[1:][0])
