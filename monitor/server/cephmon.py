#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

cephmon = Blueprint('cephmon', __name__)


@cephmon.route("/")
def get_ceph_cluster_status():
    '''
    Cluster status
    '''
    return "hello cluster status"


