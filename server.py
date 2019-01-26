import os
from aiohttp import web
from urllib.parse import parse_qs, quote
import logging
import aiohttp
import json


logging.basicConfig(level=logging.INFO)

RANCHDATA_DEST = 'https://ranchdata.net/api/v1/sensor'
API_KEY = os.environ.get('API_KEY')
SENSOR_NAME = "oregon"
MEASUREMENTS = {
    'oh': 'humidity',
    'ot': 'temperature',
}

async def handle_measurement(key, name, value):
    logging.info(name)
    logging.info(value)
    params = {
        'apikey': API_KEY,
    }
    payload = {
        'value': value
    }

    sensor_name = quote("{}/{}".format(
        SENSOR_NAME,
        name), safe='')

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "{}/{}/measurement".format(
                RANCHDATA_DEST, sensor_name
            ),
            params=params,
            data=json.dumps(payload)
        ) as resp:
            print(resp.status)

async def handle(request):
    logging.info('version request')
    return web.Response(text="ok")

async def postUpdate(request):
    logging.info('update request')
    query = await request.text()
    parsed = parse_qs(query)

    if 'oh' in parsed:
        for key in MEASUREMENTS.keys():
            await handle_measurement(
                key,
                MEASUREMENTS[key],
                parsed[key][0]
            )

    return web.Response(text="ok")

app = web.Application(debug=True)
app.add_routes([web.get('/version', handle),
                web.post('/update', postUpdate)])

web.run_app(app, port=80)

