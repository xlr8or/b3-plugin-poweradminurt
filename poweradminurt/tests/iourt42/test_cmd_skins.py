# -*- encoding: utf-8 -*-
from mock import  call, Mock
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from ..iourt42 import Iourt42TestCase


class Test_cmd_skins(Iourt42TestCase):
    def setUp(self):
        super(Test_cmd_skins, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
pagoto-goto: 20         ; set the goto <on/off>
        """)
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()

        self.console.say = Mock()
        self.console.write = Mock()

        self.moderator.connects("2")

    def test_missing_parameter(self):
        self.moderator.message_history = []
        self.moderator.says("!goto")
        self.assertListEqual(["Invalid or missing data, try !help pagoto"], self.moderator.message_history)

    def test_junk(self):
        self.moderator.message_history = []
        self.moderator.says("!goto qsdf")
        self.assertListEqual(["Invalid or missing data, try !help pagoto"], self.moderator.message_history)

    def test_on(self):
        self.moderator.says("!goto on")
        self.console.write.assert_has_calls([call('set g_allowgoto "1"')])

    def test_off(self):
        self.moderator.says("!goto off")
        self.console.write.assert_has_calls([call('set g_allowgoto "0"')])


