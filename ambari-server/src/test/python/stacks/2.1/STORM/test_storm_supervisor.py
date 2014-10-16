#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from mock.mock import MagicMock, call, patch
from stacks.utils.RMFTestCase import *
import  resource_management.core.source
from test_storm_base import TestStormBase

class TestStormSupervisor(TestStormBase):

  def test_configure_default(self):
    self.executeScript("2.1/services/STORM/package/scripts/supervisor.py",
                       classname = "Supervisor",
                       command = "configure",
                       config_file="default.json"
    )
    self.assert_configure_default()
    self.assertNoMoreResources()

  def test_start_default(self):
    self.executeScript("2.1/services/STORM/package/scripts/supervisor.py",
                       classname = "Supervisor",
                       command = "start",
                       config_file="default.json"
    )

    self.assert_configure_default()

    self.assertResourceCalled('Execute', 'env JAVA_HOME=/usr/jdk64/jdk1.7.0_45 PATH=$PATH:/usr/jdk64/jdk1.7.0_45/bin storm supervisor > /var/log/storm/supervisor.out 2>&1',
      wait_for_finish = False,
      not_if = 'ls /var/run/storm/supervisor.pid >/dev/null 2>&1 && ps `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1',
      path = ['/usr/bin'],
      user = 'storm',
    )

    self.assertResourceCalled('Execute', 'pgrep -f "^java.+backtype.storm.daemon.supervisor$" && pgrep -f "^java.+backtype.storm.daemon.supervisor$" > /var/run/storm/supervisor.pid',
      logoutput = True,
      tries = 6,
      user = 'storm',
      path = ['/usr/bin'],
      try_sleep = 10,
    )
    self.assertResourceCalled('Execute', 'env JAVA_HOME=/usr/jdk64/jdk1.7.0_45 PATH=$PATH:/usr/jdk64/jdk1.7.0_45/bin storm logviewer > /var/log/storm/logviewer.out 2>&1',
                               wait_for_finish = False,
                               not_if = 'ls /var/run/storm/logviewer.pid >/dev/null 2>&1 && ps `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1',
                               path = ['/usr/bin'],
                               user = 'storm'
    )

    self.assertResourceCalled('Execute', 'pgrep -f "^java.+backtype.storm.daemon.logviewer$" && pgrep -f "^java.+backtype.storm.daemon.logviewer$" > /var/run/storm/logviewer.pid',
                              logoutput = True,
                              tries = 12,
                              user = 'storm',
                              path = ['/usr/bin'],
                              try_sleep = 10
    )

    self.assertNoMoreResources()

  def test_stop_default(self):
    self.executeScript("2.1/services/STORM/package/scripts/supervisor.py",
                       classname = "Supervisor",
                       command = "stop",
                       config_file="default.json"
    )
    self.assertResourceCalled('Execute', 'kill `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1',
                              not_if = '! (ls /var/run/storm/supervisor.pid >/dev/null 2>&1 && ps `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1)'
    )
    self.assertResourceCalled('Execute', 'kill -9 `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1',
                              not_if = 'sleep 2; ! (ls /var/run/storm/supervisor.pid >/dev/null 2>&1 && ps `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1) || sleep 20; ! (ls /var/run/storm/supervisor.pid >/dev/null 2>&1 && ps `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1)',
                              ignore_failures=True
    )
    self.assertResourceCalled('Execute', 'rm -f /var/run/storm/supervisor.pid')
    self.assertResourceCalled('Execute', 'kill `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1',
                              not_if = '! (ls /var/run/storm/logviewer.pid >/dev/null 2>&1 && ps `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1)')

    self.assertResourceCalled('Execute', 'kill -9 `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1',
                              not_if = 'sleep 2; ! (ls /var/run/storm/logviewer.pid >/dev/null 2>&1 && ps `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1) || sleep 20; ! (ls /var/run/storm/logviewer.pid >/dev/null 2>&1 && ps `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1)',
                              ignore_failures = True)

    self.assertResourceCalled('Execute', 'rm -f /var/run/storm/logviewer.pid')
    self.assertNoMoreResources()

  def test_configure_secured(self):
    self.executeScript("2.1/services/STORM/package/scripts/supervisor.py",
                       classname = "Supervisor",
                       command = "configure",
                       config_file="secured.json"
    )
    self.assert_configure_secured()
    self.assertNoMoreResources()

  def test_start_secured(self):
    self.executeScript("2.1/services/STORM/package/scripts/supervisor.py",
                       classname = "Supervisor",
                       command = "start",
                       config_file="secured.json"
    )

    self.assert_configure_secured()

    self.assertResourceCalled('Execute', 'env JAVA_HOME=/usr/jdk64/jdk1.7.0_45 PATH=$PATH:/usr/jdk64/jdk1.7.0_45/bin storm supervisor > /var/log/storm/supervisor.out 2>&1',
      wait_for_finish = False,
      not_if = 'ls /var/run/storm/supervisor.pid >/dev/null 2>&1 && ps `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1',
      path = ['/usr/bin'],
      user = 'storm',
    )

    self.assertResourceCalled('Execute', 'pgrep -f "^java.+backtype.storm.daemon.supervisor$" && pgrep -f "^java.+backtype.storm.daemon.supervisor$" > /var/run/storm/supervisor.pid',
      logoutput = True,
      tries = 6,
      user = 'storm',
      path = ['/usr/bin'],
      try_sleep = 10,
    )
    self.assertResourceCalled('Execute', 'env JAVA_HOME=/usr/jdk64/jdk1.7.0_45 PATH=$PATH:/usr/jdk64/jdk1.7.0_45/bin storm logviewer > /var/log/storm/logviewer.out 2>&1',
                        wait_for_finish = False,
                        not_if = 'ls /var/run/storm/logviewer.pid >/dev/null 2>&1 && ps `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1',
                        path = ['/usr/bin'],
                        user = 'storm'
    )

    self.assertResourceCalled('Execute', 'pgrep -f "^java.+backtype.storm.daemon.logviewer$" && pgrep -f "^java.+backtype.storm.daemon.logviewer$" > /var/run/storm/logviewer.pid',
                        logoutput = True,
                        tries = 12,
                        user = 'storm',
                        path = ['/usr/bin'],
                        try_sleep = 10
    )
    self.assertNoMoreResources()

  def test_stop_secured(self):
    self.executeScript("2.1/services/STORM/package/scripts/supervisor.py",
                       classname = "Supervisor",
                       command = "stop",
                       config_file="secured.json"
    )
    self.assertResourceCalled('Execute', 'kill `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1',
                              not_if = '! (ls /var/run/storm/supervisor.pid >/dev/null 2>&1 && ps `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1)'
                              )
    self.assertResourceCalled('Execute', 'kill -9 `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1',
                              not_if = 'sleep 2; ! (ls /var/run/storm/supervisor.pid >/dev/null 2>&1 && ps `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1) || sleep 20; ! (ls /var/run/storm/supervisor.pid >/dev/null 2>&1 && ps `cat /var/run/storm/supervisor.pid` >/dev/null 2>&1)',
                              ignore_failures=True
    )
    self.assertResourceCalled('Execute', 'rm -f /var/run/storm/supervisor.pid')
    self.assertResourceCalled('Execute', 'kill `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1',
                              not_if = '! (ls /var/run/storm/logviewer.pid >/dev/null 2>&1 && ps `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1)')

    self.assertResourceCalled('Execute', 'kill -9 `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1',
                              not_if = 'sleep 2; ! (ls /var/run/storm/logviewer.pid >/dev/null 2>&1 && ps `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1) || sleep 20; ! (ls /var/run/storm/logviewer.pid >/dev/null 2>&1 && ps `cat /var/run/storm/logviewer.pid` >/dev/null 2>&1)',
                              ignore_failures = True)

    self.assertResourceCalled('Execute', 'rm -f /var/run/storm/logviewer.pid')
    self.assertNoMoreResources()

  def assert_configure_default(self):

    self.assertResourceCalled('Directory', '/var/log/storm',
      owner = 'storm',
      group = 'hadoop',
      recursive = True,
    )
    self.assertResourceCalled('Directory', '/var/run/storm',
      owner = 'storm',
      group = 'hadoop',
      recursive = True,
    )
    self.assertResourceCalled('Directory', '/hadoop/storm',
      owner = 'storm',
      group = 'hadoop',
      recursive = True,
    )
    self.assertResourceCalled('Directory', '/etc/storm/conf',
      owner = 'storm',
      group = 'hadoop',
      recursive = True,
    )
    self.assertResourceCalled('File', '/etc/storm/conf/config.yaml',
      owner = 'storm',
      content = Template('config.yaml.j2'),
      group = 'hadoop',
    )
    #assert that storm.yam was properly configured
    self.call_storm_template_and_assert()
    self.assertResourceCalled('File', '/etc/storm/conf/storm-env.sh',
                              owner = 'storm',
                              content = InlineTemplate(self.getConfig()['configurations']['storm-env']['content'])
                              )

  def assert_configure_secured(self):
    self.assertResourceCalled('Directory', '/var/log/storm',
      owner = 'storm',
      group = 'hadoop',
      recursive = True,
    )
    self.assertResourceCalled('Directory', '/var/run/storm',
      owner = 'storm',
      group = 'hadoop',
      recursive = True,
    )
    self.assertResourceCalled('Directory', '/hadoop/storm',
      owner = 'storm',
      group = 'hadoop',
      recursive = True,
    )
    self.assertResourceCalled('Directory', '/etc/storm/conf',
      owner = 'storm',
      group = 'hadoop',
      recursive = True,
    )
    self.assertResourceCalled('File', '/etc/storm/conf/config.yaml',
      owner = 'storm',
      content = Template('config.yaml.j2'),
      group = 'hadoop',
    )
#     self.assertResourceCalled('File', '/etc/storm/conf/storm.yaml',
#       owner = 'storm',
#       content = self.get_yaml_inline_template(self.getConfig()['configurations']['storm-site']),
#       group = 'hadoop',
#       mode = None,
#     )
    #assert that storm.yam was properly configured
    self.call_storm_template_and_assert()

    self.assertResourceCalled('File', '/etc/storm/conf/storm-env.sh',
                              owner = 'storm',
                              content = InlineTemplate(self.getConfig()['configurations']['storm-env']['content'])
                              )
    self.assertResourceCalled('TemplateConfig', '/etc/storm/conf/storm_jaas.conf',
      owner = 'storm',
    )

#   def get_yaml_inline_template(self, configurations):
#     with self.env:
#       from yaml_config import yaml_inline_template
#       from storm import enrich_kerberos_settings
#       import params
#
#       if params.security_enabled:
#         return yaml_inline_template(enrich_kerberos_settings(configurations, params.conf_dir, "EXAMPLE.COM"))
#       else:
#         return yaml_inline_template(configurations)
