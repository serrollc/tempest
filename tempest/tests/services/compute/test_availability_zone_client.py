# Copyright 2015 NEC Corporation.  All rights reserved.
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

import httplib2

from oslo_serialization import jsonutils as json
from oslotest import mockpatch

from tempest.services.compute.json import availability_zone_client
from tempest.tests import base
from tempest.tests import fake_auth_provider


class TestAvailabilityZoneClient(base.TestCase):

    FAKE_AVAILABIRITY_ZONE_INFO = [
        {
            "zoneState": {
                "available": True
            },
            "hosts": None,
            "zoneName": u'\xf4'
        }
    ]

    def setUp(self):
        super(TestAvailabilityZoneClient, self).setUp()
        fake_auth = fake_auth_provider.FakeAuthProvider()
        self.client = availability_zone_client.AvailabilityZoneClient(
            fake_auth, 'compute', 'regionOne')

    def _test_list_availability_zones(self, bytes_body=False):
        serialized_body = json.dumps({
            "availabilityZoneInfo": self.FAKE_AVAILABIRITY_ZONE_INFO})
        if bytes_body:
            serialized_body = serialized_body.encode('utf-8')

        mocked_resp = (httplib2.Response({'status': 200}), serialized_body)
        self.useFixture(mockpatch.Patch(
            'tempest.common.service_client.ServiceClient.get',
            return_value=mocked_resp))
        resp = self.client.list_availability_zones()
        self.assertEqual({
            "availabilityZoneInfo": self.FAKE_AVAILABIRITY_ZONE_INFO}, resp)

    def test_list_availability_zones_with_str_body(self):
        self._test_list_availability_zones()

    def test_list_availability_zones_with_bytes_body(self):
        self._test_list_availability_zones(bytes_body=True)