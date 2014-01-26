# -*- encoding: utf-8 -*-
#
# UrT 4.1 and UrT <4.2.018 have the same behavior regarding CVAR g_gear
#
from mock import patch, call
import time
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from tests.iourt41 import Iourt41TestCase
from tests.iourt42 import Iourt42TestCase

G_NADES = 0b000001
G_SNIPERS = 0b000010
G_SPAS = 0b000100
G_PISTOLS = 0b001000
G_RIFLES = 0b010000
G_NEGEV = 0b100000
G_ALL = 0b111111
G_NONE = 0b000000

class mixin_cmd_version(object):

    def setUp(self):
        super(mixin_cmd_version, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
pagear-gear: 20
        """)
        self.p = PoweradminurtPlugin(self.console, self.conf)

        when(self.console).getCvar('timelimit').thenReturn(Cvar('timelimit', value=20))
        when(self.console).getCvar('g_maxGameClients').thenReturn(Cvar('g_maxGameClients', value=16))
        when(self.console).getCvar('sv_maxclients').thenReturn(Cvar('sv_maxclients', value=16))
        when(self.console).getCvar('sv_privateClients').thenReturn(Cvar('sv_privateClients', value=0))
        when(self.console).getCvar('g_allowvote').thenReturn(Cvar('g_allowvote', value=0))
        when(self.console).getCvar('g_modversion').thenReturn(Cvar('g_modversion', value=self.__class__.URT_G_MODVERSION))
        self.given_forbidden_weapon_are(G_NONE)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.sleep_patcher = patch.object(time, 'sleep')
        self.sleep_patcher.start()
        self.setCvar_patcher = patch.object(self.console, 'setCvar')
        self.setCvar_mock = self.setCvar_patcher.start()

        self.superadmin.connects("2")

    def tearDown(self):
        super(mixin_cmd_version, self).tearDown()
        self.sleep_patcher.stop()
        self.setCvar_patcher.stop()

    def given_forbidden_weapon_are(self, g_gear_value):
        when(self.console).getCvar('g_gear').thenReturn(Cvar('g_gear', value=str(g_gear_value)))

    def assert_set_gear(self, expected_gear_value):
        self.assertListEqual([call('g_gear', str(expected_gear_value))], self.setCvar_mock.mock_calls)

    def test_reset(self):
        # GIVEN
        self.given_forbidden_weapon_are("1234")
        self.p.onStartup()
        # WHEN
        self.superadmin.says("!gear reset")
        # THEN
        self.assert_set_gear('1234')

    def test_all(self):
        # WHEN
        self.superadmin.says("!gear all")
        # THEN
        self.assert_set_gear(G_NONE)

    def test_none(self):
        # WHEN
        self.superadmin.says("!gear none")
        # THEN
        self.assert_set_gear(G_ALL)

    def test_forbid_nades(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_NONE)
        # WHEN
        self.superadmin.says("!gear -nade")
        # THEN
        self.assert_set_gear(G_NADES)

    def test_allow_nades(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_ALL)
        # WHEN
        self.superadmin.says("!gear +nade")
        # THEN
        self.assert_set_gear(G_ALL - G_NADES)

    def test_forbid_snipers(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_NONE)
        # WHEN
        self.superadmin.says("!gear -snip")
        # THEN
        self.assert_set_gear(G_SNIPERS)

    def test_allow_snipers(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_ALL)
        # WHEN
        self.superadmin.says("!gear +snip")
        # THEN
        self.assert_set_gear(G_ALL - G_SNIPERS)

    def test_forbid_spas(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_NONE)
        # WHEN
        self.superadmin.says("!gear -spas")
        # THEN
        self.assert_set_gear(G_SPAS)

    def test_allow_spas(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_ALL)
        # WHEN
        self.superadmin.says("!gear +spas")
        # THEN
        self.assert_set_gear(G_ALL - G_SPAS)

    def test_forbid_pistols(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_NONE)
        # WHEN
        self.superadmin.says("!gear -pist")
        # THEN
        self.assert_set_gear(G_PISTOLS)

    def test_allow_pistols(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_ALL)
        # WHEN
        self.superadmin.says("!gear +pist")
        # THEN
        self.assert_set_gear(G_ALL - G_PISTOLS)


    def test_forbid_auto(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_NONE)
        # WHEN
        self.superadmin.says("!gear -auto")
        # THEN
        self.assert_set_gear(G_RIFLES)

    def test_allow_auto(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_ALL)
        # WHEN
        self.superadmin.says("!gear +auto")
        # THEN
        self.assert_set_gear(G_ALL - G_RIFLES)

    def test_forbid_negev(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_NONE)
        # WHEN
        self.superadmin.says("!gear -negev")
        # THEN
        self.assert_set_gear(G_NEGEV)

    def test_allow_negev(self):
       # GIVEN
        self.given_forbidden_weapon_are(G_ALL)
        # WHEN
        self.superadmin.says("!gear +negev")
        # THEN
        self.assert_set_gear(G_ALL - G_NEGEV)


class Test_cmd_pagear_41(mixin_cmd_version, Iourt41TestCase):
    """
    call the mixin_cmd_pagear test using the Iourt41TestCase parent class
    """
    URT_G_MODVERSION = "4.1"

class Test_cmd_pagear_42(mixin_cmd_version, Iourt42TestCase):
    """
    call the mixin_cmd_pagear test using the Iourt42TestCase parent class
    """
    URT_G_MODVERSION = "4.2.017"
