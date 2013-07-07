# -*- encoding: utf-8 -*-
from mock import  call, Mock
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from tests.iourt42 import Iourt42TestCase


class Test_cmd_goto(Iourt42TestCase):
    def setUp(self):
        super(Test_cmd_goto, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
paskins-skins: 20       ; set the use of client skins <on/off>
        """)
        self.p = PoweradminurtPlugin(self.console, self.conf)

        when(self.console).getCvar('timelimit').thenReturn(Cvar('timelimit', value=20))
        when(self.console).getCvar('g_maxGameClients').thenReturn(Cvar('g_maxGameClients', value=16))
        when(self.console).getCvar('sv_maxclients').thenReturn(Cvar('sv_maxclients', value=16))
        when(self.console).getCvar('sv_privateClients').thenReturn(Cvar('sv_privateClients', value=0))
        when(self.console).getCvar('g_allowvote').thenReturn(Cvar('g_allowvote', value=0))
        self.p.onLoadConfig()
        self.p.onStartup()

        self.console.say = Mock()
        self.console.write = Mock()

        self.moderator.connects("2")

    def test_missing_parameter(self):
        self.moderator.message_history = []
        self.moderator.says("!skins")
        self.assertListEqual(["Invalid or missing data, try !help paskins"], self.moderator.message_history)

    def test_junk(self):
        self.moderator.message_history = []
        self.moderator.says("!skins qsdf")
        self.assertListEqual(["Invalid or missing data, try !help paskins"], self.moderator.message_history)

    def test_on(self):
        self.moderator.says("!skins on")
        self.console.write.assert_has_calls([call('set g_skins "1"')])

    def test_off(self):
        self.moderator.says("!skins off")
        self.console.write.assert_has_calls([call('set g_skins "0"')])


