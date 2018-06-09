from psd_tools import PSDImage, Group, Layer
from PIL.Image import Image
import os
import json
import sys


def layers_to_dir(layers, name='', updir='./'):
    dirname = updir + name + '/'
    os.makedirs(updir + name, exist_ok=True)

    info = {}

    for item in layers:
        if isinstance(item, Group):
            info[item.name] = {
                'type': 'group',
                'items': layers_to_dir(item.layers, item.name, dirname),
            }
        if isinstance(item, Layer):
            info[item.name] = {
                'type': 'layer',
                'x1': item.bbox.x1,
                'y1': item.bbox.y1,
                'x2': item.bbox.x2,
                'y2': item.bbox.y2,
            }

            img = item.as_PIL()  # type: Image
            with open('%s/%s.png' % (dirname, item.name), 'bw') as io:
                img.save(io, 'png')

    return info


def unpack(path):
    _, filename = os.path.split(path)
    name = filename[:filename.rfind('.')]
    psd = PSDImage.load(path)
    info = layers_to_dir(psd.layers, name)
    with open('%s/info.json' % name, 'w') as io:
        json.dump(info, io, ensure_ascii=False)


files = sys.argv[1:]
for file in files:
    unpack(file)
