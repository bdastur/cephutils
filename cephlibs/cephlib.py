#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import rados
#import pprint



class Cephlib(object):
    '''
    A wrapper lib for rados.
    '''
    def __init__(self, cephconf):
        print "Cephlib init"
        self.ceph_configfile = cephconf
        try:
            self.cluster = rados.Rados(conffile=cephconf)
            self.cluster.connect()
        except rados.Error as err:
            print "Rados Error: connect failed [%s]" % err

    def get_cluster_summary_json(self):
        '''
        Get the Cluster summary
        '''

        cmd = {"prefix": "status", "format": "json"}
        try:
            ret, buf, err = self.cluster.mon_command(json.dumps(cmd), "")
        except rados.Error as err:
            print "Rados Error: [get cluster summary] [%s]" % err
            return None

        return buf

    def get_ceph_osd_stat_json(self):
        '''
        Get the osd stat output
        '''
        cmd = {"prefix": "osd stat", "format": "json"}
        try:
            ret, buf, err = self.cluster.mon_command(json.dumps(cmd), "")
        except rados.Error as err:
            print "Rados Error: [get osd stat] [%s]" % err
            return None

        return buf

    def get_ceph_osd_df_json(self):
        '''
        Get ceph osd df output
        '''
        cmd = {"prefix": "osd df", "format": "json"}
        try:
            ret, buf, err = self.cluster.mon_command(json.dumps(cmd), "")
        except rados.Error as err:
            print "Rados Error: [get osd dump] [%s]" % err
            return None

        return buf

    def get_ceph_osd_count(self):
        '''
        Get the Total, up, in osds
        '''
        data = self.get_ceph_osd_stat_json()
        dictdata = json.loads(data)
        try:
            (total_osds, up_osds, in_osds) = \
                (dictdata['num_osds'],
                 dictdata['num_up_osds'],
                 dictdata['num_in_osds'])

        except KeyError as err:
            print "KeyError [%s] " % err
            return (None, None, None)

        return (int(total_osds), int(up_osds), int(in_osds))

    def get_cluster_health(self):
        '''
        Get the clsuter health
        '''
        data = self.get_cluster_summary_json()
        dictdata = json.loads(data)

        try:
            health_status = dictdata['health']['overall_status']
        except KeyError as err:
            print "KeyError [%s] " % err
            return None

        return health_status




