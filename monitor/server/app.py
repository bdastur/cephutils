#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import jsonify
import json
import rados
import sys
import pprint


app = Flask(__name__)
CONFFILE = "/etc/ceph/ceph.conf"


class Cephmon(object):
    __instance = None
    __cluster = None

    def __new__(cls):
        if cls.__instance is None:
            print "Initialize class"
            cls.__instance = object.__new__(cls)
            cls.__instance.name = "Ceph mon"
            try:
                cls.__cluster = rados.Rados(conffile=CONFFILE)
                cls.__cluster.connect()
            except rados.Error as err:
                print "Rados client failure [%s]" % err
        return cls.__instance

    def __init__(self):
        print "init called"
        self.cluster = None

    def get_cluster_summary(self):
        print "get cluster summary"

        cmd = {"prefix": "status", "format": "json"}
        try:
            ret, buf, err = self.__cluster.mon_command(json.dumps(cmd), "")
        except rados.Error as err:
            print "ERROR: Get cluster summary [%s] " % err
            return None

        print "Ret: %s , Err: %s" % (str(ret), str(err))

        return json.loads(buf)


@app.route("/")
def get_ceph_cluster_status():
    '''
    Ceph Cluster Status API
    '''
    cluster_summary = {}

    cephmon = Cephmon()

    cluster_summary = cephmon.get_cluster_summary()
    print "cluster summary: ", cluster_summary

    mimetype = request.headers.get("mimetype", None)

    if mimetype == "application/json":
        print "Json data"
        return jsonify(cluster_summary)
    else:
        # Could return a rendered template here.
        return jsonify(cluster_summary)


def main():
    app.run(host="0.0.0.0", port=5001, debug=True)

if __name__ == '__main__':
    main()
