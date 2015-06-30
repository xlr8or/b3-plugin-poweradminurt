# -*- encoding: utf-8 -*-
from mock import patch, Mock, call
import time
from mockito import when
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from poweradminurt import PoweradminurtPlugin
from ..iourt41 import Iourt41TestCase
from ..iourt42 import Iourt42TestCase
from poweradminurt import __version__ as plugin_version, __author__ as plugin_author


class mixin_cmd_paset(object):
    def setUp(self):
        super(mixin_cmd_paset, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
paset: 20
        """)
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()

        self.sleep_patcher = patch.object(time, 'sleep')
        self.sleep_patcher.start()
        self.setCvar_patcher = patch.object(self.console, 'setCvar')
        self.setCvar_mock = self.setCvar_patcher.start()

        self.moderator.connects("2")

    def assert_setCvar_calls(self, expected_calls):
        self.assertListEqual(expected_calls, self.setCvar_mock.mock_calls)

    def tearDown(self):
        super(mixin_cmd_paset, self).tearDown()
        self.sleep_patcher.stop()
        self.setCvar_patcher.stop()


    def test_nominal(self):
        # WHEN
        self.moderator.says('!paset sv_foo bar')
        # THEN
        self.assert_setCvar_calls([call('sv_foo', 'bar')])
        self.assertListEqual([], self.moderator.message_history)

    def test_no_parameter(self):
        # WHEN
        self.moderator.says('!paset')
        # THEN
        self.assert_setCvar_calls([])
        self.assertListEqual(['Invalid or missing data, try !help paset'], self.moderator.message_history)

    def test_no_value(self):
        # WHEN
        self.moderator.says('!paset sv_foo')
        # THEN
        self.assert_setCvar_calls([call('sv_foo', '')])
        self.assertListEqual([], self.moderator.message_history)


class Test_cmd_nuke_41(mixin_cmd_paset, Iourt41TestCase):
    """
    call the mixin test using the Iourt41TestCase parent class
    """

class Test_cmd_nuke_42(mixin_cmd_paset, Iourt42TestCase):
    """
    call the mixin test using the Iourt42TestCase parent class
    """
