# -*- encoding: utf-8 -*-
from mock import patch, Mock
import time
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from ..iourt41 import Iourt41TestCase
from ..iourt42 import Iourt42TestCase
from poweradminurt import __version__ as plugin_version, __author__ as plugin_author


class mixin_cmd_version(object):
    def setUp(self):
        super(mixin_cmd_version, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
paversion-version: 20
        """)
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()

        self.sleep_patcher = patch.object(time, 'sleep')
        self.sleep_patcher.start()

        self.console.say = Mock()
        self.console.saybig = Mock()
        self.console.write = Mock()

        self.moderator.connects("2")


    def tearDown(self):
        super(mixin_cmd_version, self).tearDown()
        self.sleep_patcher.stop()


    def test_nominal(self):
        self.moderator.message_history = []
        self.moderator.says("!version")
        self.assertEqual(['I am PowerAdminUrt version %s by %s' % (plugin_version, plugin_author)], self.moderator.message_history)



class Test_cmd_nuke_41(mixin_cmd_version, Iourt41TestCase):
    """
    call the mixin_cmd_nuke test using the Iourt41TestCase parent class
    """

class Test_cmd_nuke_42(mixin_cmd_version, Iourt42TestCase):
    """
    call the mixin_cmd_nuke test using the Iourt42TestCase parent class
    """
