# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Controllers related to user subscriptions."""

from __future__ import absolute_import
from __future__ import unicode_literals

from core import feconf
from core.controllers import acl_decorators
from core.controllers import base
from core.domain import subscription_services
from core.domain import user_services


class SubscribeHandler(base.BaseHandler):
    """Handles operations relating to new subscriptions."""

    POST_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON
    URL_PATH_ARGS_SCHEMAS = {}
    HANDLER_ARGS_SCHEMAS = {
        'POST': {
            'creator_username': {
                'schema': {
                    'type': 'basestring',
                    'validators': [{
                        'id': 'is_valid_username_string'
                    }]
                }
            }
        }
    }

    @acl_decorators.can_subscribe_to_users
    def post(self):
        creator_id = user_services.get_user_id_from_username(
            self.normalized_payload.get('creator_username'))
        subscription_services.subscribe_to_creator(self.user_id, creator_id)
        self.render_json(self.values)


class UnsubscribeHandler(base.BaseHandler):
    """Handles operations related to unsubscriptions."""

    POST_HANDLER_ERROR_RETURN_TYPE = feconf.HANDLER_TYPE_JSON
    URL_PATH_ARGS_SCHEMAS = {}
    HANDLER_ARGS_SCHEMAS = {
        'POST': {
            'creator_username': {
                'schema': {
                    'type': 'basestring',
                    'validators': [{
                        'id': 'is_valid_username_string'
                    }]
                }
            }
        }
    }

    @acl_decorators.can_subscribe_to_users
    def post(self):
        creator_id = user_services.get_user_id_from_username(
            self.normalized_payload.get('creator_username'))
        subscription_services.unsubscribe_from_creator(
            self.user_id, creator_id)
        self.render_json(self.values)
