# Copyright 2013 IBM Corporation
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

from lxml import etree

from tempest.common.rest_client import RestClientXML
from tempest import config
from tempest.services.compute.xml.common import xml_to_json

CONF = config.CONF


class InstanceUsagesAuditLogClientXML(RestClientXML):

    def __init__(self, auth_provider):
        super(InstanceUsagesAuditLogClientXML, self).__init__(
            auth_provider)
        self.service = CONF.compute.catalog_type

    def list_instance_usage_audit_logs(self):
        url = 'os-instance_usage_audit_log'
        resp, body = self.get(url, self.headers)
        instance_usage_audit_logs = xml_to_json(etree.fromstring(body))
        return resp, instance_usage_audit_logs

    def get_instance_usage_audit_log(self, time_before):
        url = 'os-instance_usage_audit_log/%s' % time_before
        resp, body = self.get(url, self.headers)
        instance_usage_audit_log = xml_to_json(etree.fromstring(body))
        return resp, instance_usage_audit_log
