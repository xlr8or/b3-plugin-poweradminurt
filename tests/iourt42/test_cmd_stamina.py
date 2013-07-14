# -*- encoding: utf-8 -*-
from mock import  call, Mock
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from tests.iourt42 import Iourt42TestCase


class Test_cmd_funstuff(Iourt42TestCase):
    def setUp(self):
        super(Test_cmd_funstuff, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
pastamina-stamina: 20   ; set the stamina behavior <default/regain/infinite>
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
        self.moderator.says("!stamina")
        self.assertListEqual(["Invalid or missing data, try !help pastamina"], self.moderator.message_history)

    def test_junk(self):
        self.moderator.message_history = []
        self.moderator.says("!stamina qsdf")
        self.assertListEqual(["Invalid or missing data, try !help pastamina"], self.moderator.message_history)

    def test_default(self):
        self.moderator.says("!stamina default")
        self.console.write.assert_has_calls([call('set g_stamina "0"')])

    def test_regain(self):
        self.moderator.says("!stamina regain")
        self.console.write.assert_has_calls([call('set g_stamina "1"')])

    def test_infinite(self):
        self.moderator.says("!stamina infinite")
        self.console.write.assert_has_calls([call('set g_stamina "2"')])


