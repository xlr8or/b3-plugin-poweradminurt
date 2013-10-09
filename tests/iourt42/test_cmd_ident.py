# -*- encoding: utf-8 -*-
from mock import  call, Mock, patch
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from tests.iourt42 import Iourt42TestCase


class Test_cmd_ident(Iourt42TestCase):
    def setUp(self):
        super(Test_cmd_ident, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
paident-id: 20

[special]
paident_full_level: 40
        """)
        self.p = PoweradminurtPlugin(self.console, self.conf)

        when(self.console).getCvar('timelimit').thenReturn(Cvar('timelimit', value=20))
        when(self.console).getCvar('g_maxGameClients').thenReturn(Cvar('g_maxGameClients', value=16))
        when(self.console).getCvar('sv_maxclients').thenReturn(Cvar('sv_maxclients', value=16))
        when(self.console).getCvar('sv_privateClients').thenReturn(Cvar('sv_privateClients', value=0))
        when(self.console).getCvar('g_allowvote').thenReturn(Cvar('g_allowvote', value=0))
        self.parser_conf._settings.update({'b3': {"time_zone": "GMT", "time_format": "%I:%M%p %Z %m/%d/%y"}})
        self.p.onLoadConfig()
        self.p.onStartup()

        self.console.say = Mock()
        self.console.write = Mock()

        self.moderator.connects("2")
        self.moderator.message_history = []

    def test_no_parameter(self):
        # WHEN
        self.moderator.says("!id")
        # THEN
        self.assertListEqual(["Your id is @2"], self.moderator.message_history)

    def test_junk(self):
        # WHEN
        self.moderator.says("!id qsdfsqdq sqfd qf")
        # THEN
        self.assertListEqual(["No players found matching qsdfsqdq"], self.moderator.message_history)

    def test_nominal_under_full_level(self):
        # GIVEN
        self.joe.pbid = "joe_pbid"
        self.joe.connects('3')
        # WHEN
        with patch('time.time', return_value=0.0) as time_mock:
            self.moderator.says("!id joe")
        # THEN
        self.assertListEqual(['12:00AM GMT 01/01/70 @3 Joe'], self.moderator.message_history)

    def test_nominal_above_full_level(self):
        # GIVEN
        self.joe.pbid = "joe_pbid"
        self.joe.connects('3')
        self.joe.timeAdd = 90*60.0
        self.superadmin.connects('1')
        # WHEN
        with patch('time.time', return_value=180*60.0):
            self.superadmin.says("!id joe")
        # THEN
        self.assertListEqual(['03:00AM GMT 01/01/70 @3 Joe  [joe_pbid] since 01:30AM GMT 01/01/70'], self.superadmin.message_history)


