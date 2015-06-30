# -*- encoding: utf-8 -*-
from b3 import TEAM_RED
from b3 import TEAM_BLUE
from mock import  call, Mock
from b3.config import CfgConfigParser
from poweradminurt import PoweradminurtPlugin
from ..iourt42 import Iourt42TestCase


class Test_cmd_swap(Iourt42TestCase):
    def setUp(self):
        super(Test_cmd_swap, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
paswap-swap: 20
        """)
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()
        self.console.say = Mock()
        self.console.write = Mock()
        self.admin.connects("2")
        self.moderator.connects("3")

    def test_plugin_using_overridden_command_method(self):
        self.admin.team = TEAM_RED
        self.moderator.team = TEAM_BLUE
        self.admin.says("!swap 2 3")
        self.console.write.assert_has_calls([call('swap %s %s' % (self.admin.cid, self.moderator.cid))])
