# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
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

from testtools import matchers

from tempest.api.volume import base
from tempest import clients
from tempest import config
from tempest import test

CONF = config.CONF


class VolumesTransfersTest(base.BaseVolumeV1Test):
    _interface = "json"

    @classmethod
    def setUpClass(cls):
        super(VolumesTransfersTest, cls).setUpClass()

        # Add another tenant to test volume-transfer
        if CONF.compute.allow_tenant_isolation:
            cls.os_alt = clients.Manager(cls.isolated_creds.get_alt_creds(),
                                         interface=cls._interface)
            # Add admin tenant to cleanup resources
            cls.os_adm = clients.Manager(cls.isolated_creds.get_admin_creds(),
                                         interface=cls._interface)
        else:
            cls.os_alt = clients.AltManager()
            cls.os_adm = clients.ComputeAdminManager(interface=cls._interface)

        cls.client = cls.volumes_client
        cls.alt_client = cls.os_alt.volumes_client
        cls.alt_tenant_id = cls.alt_client.tenant_id
        cls.adm_client = cls.os_adm.volumes_client

    def _delete_volume(self, volume_id):
        # Delete the specified volume using admin creds
        resp, _ = self.adm_client.delete_volume(volume_id)
        self.assertEqual(202, resp.status)
        self.adm_client.wait_for_resource_deletion(volume_id)

    @test.attr(type='gate')
    def test_create_get_list_accept_volume_transfer(self):
        # Create a volume first
        volume = self.create_volume()
        self.addCleanup(self._delete_volume, volume['id'])

        # Create a volume transfer
        resp, transfer = self.client.create_volume_transfer(volume['id'])
        self.assertEqual(202, resp.status)
        transfer_id = transfer['id']
        auth_key = transfer['auth_key']
        self.client.wait_for_volume_status(volume['id'],
                                           'awaiting-transfer')

        # Get a volume transfer
        resp, body = self.client.get_volume_transfer(transfer_id)
        self.assertEqual(200, resp.status)
        self.assertEqual(volume['id'], body['volume_id'])

        # List volume transfers, the result should be greater than
        # or equal to 1
        resp, body = self.client.list_volume_transfers()
        self.assertEqual(200, resp.status)
        self.assertThat(len(body), matchers.GreaterThan(0))

        # Accept a volume transfer by alt_tenant
        resp, body = self.alt_client.accept_volume_transfer(transfer_id,
                                                            auth_key)
        self.assertEqual(202, resp.status)
        self.alt_client.wait_for_volume_status(volume['id'], 'available')

    def test_create_list_delete_volume_transfer(self):
        # Create a volume first
        volume = self.create_volume()
        self.addCleanup(self._delete_volume, volume['id'])

        # Create a volume transfer
        resp, body = self.client.create_volume_transfer(volume['id'])
        self.assertEqual(202, resp.status)
        transfer_id = body['id']
        self.client.wait_for_volume_status(volume['id'],
                                           'awaiting-transfer')

        # List all volume transfers (looking for the one we created)
        resp, body = self.client.list_volume_transfers()
        self.assertEqual(200, resp.status)
        for transfer in body:
            if volume['id'] == transfer['volume_id']:
                break
        else:
            self.fail('Transfer not found for volume %s' % volume['id'])

        # Delete a volume transfer
        resp, body = self.client.delete_volume_transfer(transfer_id)
        self.assertEqual(202, resp.status)
        self.client.wait_for_volume_status(volume['id'], 'available')


class VolumesTransfersTestXML(VolumesTransfersTest):
    _interface = "xml"
