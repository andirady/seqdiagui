import json
import os
import random
from string import ascii_letters, digits
from bottle import route, run, request, response, static_file
from seqdiag.command import SeqdiagApp


CHARS = ascii_letters + digits
APP = SeqdiagApp()


def random_string(n):
    return ''.join(random.choice(CHARS) for i in range(n))


@route('/')
def index():
    with open('public/index.html') as f:
        response.set_cookie('sid', random_string(16))
        return f.read()


@route('/draw', method='POST')
def draw():
    sid = request.get_cookie('sid')
    name = f'{random_string(8)}'
    direc = f'tmp/{sid}'
    if not os.path.isdir(direc):
        os.makedirs(direc)
    fn = f'{direc}/{name}.diag'
    with open(fn, 'wb') as f:
        body = request.body.read()
        if len(body) == 0:
            return json.dumps({ "error": { "code": 99 } })
        f.write(body)
    rc = APP.run([f"--size={request.query['w']}x{request.query['h']}", fn])
    if rc != 0:
        return json.dumps({ "error": { "code": rc } })
    return json.dumps({ "src": f'/results/{name}.png' })


@route('/results/<fn>', method='GET')
def results(fn):
    sid = request.get_cookie('sid')
    return static_file(fn, root=os.path.join('tmp', sid))


if __name__ == '__main__':
    run()
