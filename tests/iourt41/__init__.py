import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from mockito import when
from b3 import TEAM_UNKNOWN
from b3.config import XmlConfigParser
from b3.parsers.iourt41 import Iourt41Parser
from b3.plugins.admin import AdminPlugin
from tests import logging_disabled


class Iourt41TestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Iourt41 parser specific features
    """

    @classmethod
    def setUpClass(cls):
        with logging_disabled():
            from b3.parsers.q3a.abstractParser import AbstractParser
            from b3.fake import FakeConsole
            AbstractParser.__bases__ = (FakeConsole,)
            # Now parser inheritance hierarchy is :
            # Iourt41Parser -> abstractParser -> FakeConsole -> Parser

    def setUp(self):
        with logging_disabled():
            # create a Iourt41 parser
            self.parser_conf = XmlConfigParser()
            self.parser_conf.loadFromString("""<configuration><settings name="server"><set name="game_log"></set></settings></configuration>""")
            self.console = Iourt41Parser(self.parser_conf)
            self.console.startup()

            # load the admin plugin
            self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.xml')
            self.adminPlugin.onStartup()

            # make sure the admin plugin obtained by other plugins is our admin plugin
            when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)

            # prepare a few players
            from b3.fake import FakeClient
            self.joe = FakeClient(self.console, name="Joe", exactName="Joe", guid="zaerezarezar", groupBits=1, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.simon = FakeClient(self.console, name="Simon", exactName="Simon", guid="qsdfdsqfdsqf", groupBits=0, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.reg = FakeClient(self.console, name="Reg", exactName="Reg", guid="qsdfdsqfdsqf33", groupBits=4, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.moderator = FakeClient(self.console, name="Moderator", exactName="Moderator", guid="sdf455ezr", groupBits=8, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.admin = FakeClient(self.console, name="Level-40-Admin", exactName="Level-40-Admin", guid="875sasda", groupBits=16, team=TEAM_UNKNOWN, teamId=0, squad=0)
            self.superadmin = FakeClient(self.console, name="God", exactName="God", guid="f4qfer654r", groupBits=128, team=TEAM_UNKNOWN, teamId=0, squad=0)

    def tearDown(self):
        self.console.working = False
#        sys.stdout.write("\tactive threads count : %s " % threading.activeCount())
#        sys.stderr.write("%s\n" % threading.enumerate())
