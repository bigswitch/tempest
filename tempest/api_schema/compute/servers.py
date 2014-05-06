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

get_password = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'password': {'type': 'string'}
        },
        'required': ['password']
    }
}

get_vnc_console = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'console': {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'url': {
                        'type': 'string',
                        'format': 'uri'
                    }
                },
                'required': ['type', 'url']
            }
        },
        'required': ['console']
    }
}

base_update_server = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'server': {
                'type': 'object',
                'properties': {
                    'id': {'type': ['integer', 'string']},
                    'name': {'type': 'string'},
                    'status': {'type': 'string'},
                    'image': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': ['integer', 'string']},
                            'links': parameter_types.links
                        },
                        'required': ['id', 'links']
                    },
                    'flavor': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': ['integer', 'string']},
                            'links': parameter_types.links
                        },
                        'required': ['id', 'links']
                    },
                    'user_id': {'type': 'string'},
                    'tenant_id': {'type': 'string'},
                    'created': {'type': 'string'},
                    'updated': {'type': 'string'},
                    'progress': {'type': 'integer'},
                    'metadata': {'type': 'object'},
                    'links': parameter_types.links,
                    'addresses': parameter_types.addresses,
                },
                'required': ['id', 'name', 'status', 'image', 'flavor',
                             'user_id', 'tenant_id', 'created', 'updated',
                             'progress', 'metadata', 'links', 'addresses']
            }
        }
    }
}

delete_server = {
    'status_code': [204],
}

set_server_metadata = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'metadata': {
                'type': 'object',
                'patternProperties': {
                    '^.+$': {'type': 'string'}
                }
            }
        },
        'required': ['metadata']
    }
}

list_server_metadata = copy.deepcopy(set_server_metadata)

delete_server_metadata_item = {
    'status_code': [204]
}
