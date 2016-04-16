#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import cephlibs.cephlib as lib


class CephlibUt(unittest.TestCase):

    def init_cephlib(self):
        conffile = "/etc/ceph/ceph.conf"
        testlib = lib.Cephlib(conffile)
        return testlib

    def test_ceph_summary(self):
        print "test ceph summary api"
        cephlib = self.init_cephlib()

        data = cephlib.get_cluster_summary_json()
        print "Data: ", data

    def test_ceph_get_cluster_health(self):
        print "test cluster health api"

        testlib = self.init_cephlib()
        status = testlib.get_cluster_health()
        print "status: ", status

    def test_get_ceph_osd_stat_json(self):
        print "test get_ceph_osd_stat_json"
        testlib = self.init_cephlib()
        data = testlib.get_ceph_osd_stat_json()
        print "data: ", data

    def test_get_ceph_osd_count(self):
        print "test_get_ceph_osd_count"
        testlib = self.init_cephlib()
        (totalosd, inosd, outosd) = testlib.get_ceph_osd_count()

        print "total: %d, in: %d, out: %d" % (totalosd, inosd, outosd)

