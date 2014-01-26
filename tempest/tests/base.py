# Copyright 2013 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

import fixtures
import mock
import testtools

from tempest.openstack.common.fixture import moxstubout


class TestCase(testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        if (os.environ.get('OS_STDOUT_CAPTURE') == 'True' or
                os.environ.get('OS_STDOUT_CAPTURE') == '1'):
            stdout = self.useFixture(fixtures.StringStream('stdout')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stdout', stdout))
        if (os.environ.get('OS_STDERR_CAPTURE') == 'True' or
                os.environ.get('OS_STDERR_CAPTURE') == '1'):
            stderr = self.useFixture(fixtures.StringStream('stderr')).stream
            self.useFixture(fixtures.MonkeyPatch('sys.stderr', stderr))

        mox_fixture = self.useFixture(moxstubout.MoxStubout())
        self.mox = mox_fixture.mox
        self.stubs = mox_fixture.stubs

    def patch(self, target, **kwargs):
        """
        Returns a started `mock.patch` object for the supplied target.

        The caller may then call the returned patcher to create a mock object.

        The caller does not need to call stop() on the returned
        patcher object, as this method automatically adds a cleanup
        to the test class to stop the patcher.

        :param target: String module.class or module.object expression to patch
        :param **kwargs: Passed as-is to `mock.patch`. See mock documentation
                         for details.
        """
        p = mock.patch(target, **kwargs)
        m = p.start()
        self.addCleanup(p.stop)
        return m
