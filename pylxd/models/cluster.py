# Copyright (c) 2016 Canonical Ltd
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
from pylxd.models import _model as model
from pylxd import managers


class Cluster(model.Model):
    """A LXD certificate."""

    server_name = model.Attribute(readonly=True)
    enabled = model.Attribute(readonly=True)

    members = model.Manager()

    # name = model.Attribute(readonly=True)
    # url = model.Attribute(readonly=True)
    # database = model.Attribute(readonly=True)
    # state = model.Attribute(readonly=True)
    # server_name = model.Attribute(readonly=True)
    # status = model.Attribute(readonly=True)
    # message = model.Attribute(readonly=True)

    def __init__(self, *args, **kwargs):
        super(Cluster, self).__init__(*args, **kwargs)

        self.members = ClusterMemberManager(self)


    @classmethod
    def get(cls, client):
        """Get a certificate by fingerprint."""

        client.assert_has_api_extension('clustering')
        response = client.api.cluster.get()

        return cls(client, **response.json()['metadata'])

    @property
    def api(self):
        print("in api:", type( self.client.api.cluster), " other type",  type(self.client.api.cluster[0]))
        print("in api:", self.client.api.cluster._api_endpoint, " other type",  self.client.api.cluster[0]._api_endpoint)
        return self.client.api.cluster
        # return self.client.api.cluster


class ClusterMemberManager(managers.BaseManager):
    manager_for = 'pylxd.models.ClusterMember'


class ClusterMember(model.Model):
    name = model.Attribute(readonly=True)
    url = model.Attribute(readonly=True)
    database = model.Attribute(readonly=True)
    state = model.Attribute(readonly=True)
    server_name = model.Attribute(readonly=True)
    status = model.Attribute(readonly=True)
    message = model.Attribute(readonly=True)

    cluster = model.Parent()

    @property
    def api(self):
        print("in member api:",type(self))
        print("in member api:",dir(self))
        print("in member api:",self.__dir__())
        print("in member api:",self.__attributes__)
        print("in member api:",self.cluster._api_endpoint)
        print("in member api[0]:",type(self.cluster[0]))
        print("in member api[0]:",self.cluster[0]._api_endpoint)
        return self.cluster.api.members[self.name]

    @classmethod
    def get(cls, cluster, name):
        """Get a certificate by fingerprint."""
        print("here")
        #response = cluster.api.members[name].get()

        #return cls(cluster.client, **response.json()['metadata'])
        return cls(cluster.client, **response.json()['metadata'])

    @classmethod
    def all(cls, cluster):
        response = cluster.api.members.get()

        nodes = []
        for node in response.json()['metadata']:
            name = node.split('/')[-1]
            nodes.append(cls(cluster.client, name=name))
        return nodes
