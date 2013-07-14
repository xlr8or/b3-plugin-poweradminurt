# -*- encoding: utf-8 -*-
from mock import  call, Mock
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from tests.iourt42 import Iourt42TestCase


class Test_cmd_skins(Iourt42TestCase):
    def setUp(self):
        super(Test_cmd_skins, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
pagoto-goto: 20         ; set the goto <on/off>
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


