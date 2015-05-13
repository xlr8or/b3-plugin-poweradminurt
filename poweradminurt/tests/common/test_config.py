# -*- encoding: utf-8 -*-
import logging

from poweradminurt import PoweradminurtPlugin
from b3.config import CfgConfigParser
from ..iourt41 import Iourt41TestCase
from ..iourt42 import Iourt42TestCase

class mixin_conf(object):

    def setUp(self):
        super(mixin_conf, self).setUp()
        self.conf = CfgConfigParser()
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        logger = logging.getLogger('output')
        logger.setLevel(logging.INFO)

    def test_empty_config(self):
        self.conf.loadFromString("""
[foo]
        """)
        self.p.onLoadConfig()
        # should not raise any error

    ####################################### matchmode #######################################

    def test_matchmode__plugins_disable(self):
        # empty
        self.conf.loadFromString("""
[matchmode]
plugins_disable:
        """)
        self.p.loadMatchMode()
        self.assertEqual([], self.p._match_plugin_disable)

        # one element
        self.conf.loadFromString("""
[matchmode]
plugins_disable: foo
        """)
        self.p.loadMatchMode()
        self.assertEqual(['foo'], self.p._match_plugin_disable)

        # many
        self.conf.loadFromString("""
[matchmode]
plugins_disable: foo, bar
        """)
        self.p.loadMatchMode()
        self.assertEqual(['foo', 'bar'], self.p._match_plugin_disable)


##############################################################################
class Test_41(mixin_conf, Iourt41TestCase):
    """
    call the mixin tests using the Iourt41TestCase parent class
    """

class Test_42(mixin_conf, Iourt42TestCase):
    """
    call the mixin tests using the Iourt42TestCase parent class
    """
