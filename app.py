import json
import os
from base64 import b64encode
from bottle import route, run, request, static_file
from seqdiag.builder import ScreenNodeBuilder
from seqdiag.drawer import DiagramDraw
from seqdiag.parser import parse_string


@route('/')
def index():
    return static_file('index.html', root='public')


@route('/draw', method='POST')
def draw():
    try:
        tree = parse_string(request.body.read().decode('UTF-8'))
    except Exception as e:
        print("ERROR:", e)
        return json.dumps({ "error": { "code": -1 } })

    diag = ScreenNodeBuilder.build(tree)
    draw = DiagramDraw("png", diag)
    draw.draw()
    raw = draw.save()
    return json.dumps({ "src": f"data:image/png;base64,{b64encode(raw).decode('UTF-8')}" })


if __name__ == '__main__':
    run()
