# Copyright 2014 NEC Corporation.  All rights reserved.
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

import copy

from tempest.api_schema.compute import parameter_types
from tempest.api_schema.compute import servers

create_server = {
    'status_code': [202],
    'response_body': {
        'type': 'object',
        'properties': {
            'server': {
                'type': 'object',
                'properties': {
                    # NOTE: Now the type of 'id' is uuid, but here allows
                    # 'integer' also because old OpenStack uses 'integer'
                    # as a server id.
                    'id': {'type': ['integer', 'string']},
                    'os-security-groups:security_groups': {'type': 'array'},
                    'links': parameter_types.links,
                    'admin_password': {'type': 'string'},
                    'os-access-ips:access_ip_v4': parameter_types.access_ip_v4,
                    'os-access-ips:access_ip_v6': parameter_types.access_ip_v6
                },
                # NOTE: os-access-ips:access_ip_v4/v6 are API extension,
                # and some environments return a response without these
                # attributes. So they are not 'required'.
                'required': ['id', 'os-security-groups:security_groups',
                             'links', 'admin_password']
            }
        },
        'required': ['server']
    }
}

addresses_v3 = copy.deepcopy(parameter_types.addresses)
addresses_v3['patternProperties']['^[a-zA-Z0-9-_.]+$']['items'][
    'properties'].update({
        'type': {'type': 'string'},
        'mac_addr': {'type': 'string'}
    })
addresses_v3['patternProperties']['^[a-zA-Z0-9-_.]+$']['items'][
    'required'].extend(
        ['type', 'mac_addr']
    )

update_server = copy.deepcopy(servers.base_update_server)
update_server['response_body']['properties']['server']['properties'].update({
    'addresses': addresses_v3,
    'host_id': {'type': 'string'},
    'os-access-ips:access_ip_v4': parameter_types.access_ip_v4,
    'os-access-ips:access_ip_v6': parameter_types.access_ip_v6
})
update_server['response_body']['properties']['server']['required'].append(
    # NOTE: os-access-ips:access_ip_v4/v6 are API extension,
    # and some environments return a response without these
    # attributes. So they are not 'required'.
    'host_id'
)

attach_detach_volume = {
    'status_code': [202]
}

set_get_server_metadata_item = copy.deepcopy(servers.set_server_metadata)
