import os
import xml.etree.ElementTree as ET

import requests

from app.ev import EV

def get_tree_from_icecast():
    icecast_URL = 'http://npl.streamguys1.com:/admin/stats.xml'

    tree = requests.get(icecast_URL, auth=(EV().icecast_user, EV().icecast_pass))
    if tree.status_code == 200:
        return tree.text
    else: return 'hmmmmm'

def parse_icecast_tree():
    tree = get_tree_from_icecast()
    tree = ET.fromstring(tree)
    mountpoints = tree.findall('source')
    for mount in mountpoints:
        if mount.get('mount') == '/live':
            now_playing = mount.find('yp_currently_playing')
            return now_playing.text

def icecast_now_playing():
    return parse_icecast_tree()
