# -*- encoding: utf-8 -*-
from mock import  call, Mock
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from ..iourt42 import Iourt42TestCase


class Test_cmd_funstuff(Iourt42TestCase):
    def setUp(self):
        super(Test_cmd_funstuff, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
pafunstuff-funstuff: 20 ; set the use of funstuff <on/off>
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
        self.moderator.says("!funstuff")
        self.assertListEqual(["Invalid or missing data, try !help pafunstuff"], self.moderator.message_history)

    def test_junk(self):
        self.moderator.message_history = []
        self.moderator.says("!funstuff qsdf")
        self.assertListEqual(["Invalid or missing data, try !help pafunstuff"], self.moderator.message_history)

    def test_on(self):
        self.moderator.says("!funstuff on")
        self.console.write.assert_has_calls([call('set g_funstuff "1"')])

    def test_off(self):
        self.moderator.says("!funstuff off")
        self.console.write.assert_has_calls([call('set g_funstuff "0"')])


