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

"""Registry for typed objects."""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy
import inspect
import json

from core import feconf
from core import python_utils
from extensions.objects.models import objects


class Registry:
    """Registry of all objects."""

    # Dict mapping object class names to their classes.
    objects_dict = {}

    @classmethod
    def _refresh_registry(cls):
        """Refreshes the registry by adding new object classes to the
        registry.
        """
        cls.objects_dict.clear()

        # Add new object instances to the registry.
        for name, clazz in inspect.getmembers(
                objects, predicate=inspect.isclass):
            if name == 'BaseObject':
                continue

            ancestor_names = [
                base_class.__name__ for base_class in inspect.getmro(clazz)]

            assert 'BaseObject' in ancestor_names
            cls.objects_dict[clazz.__name__] = clazz

    @classmethod
    def get_all_object_classes(cls):
        """Get the dict of all object classes."""
        cls._refresh_registry()
        return copy.deepcopy(cls.objects_dict)

    @classmethod
    def get_object_class_by_type(cls, obj_type):
        """Gets an object class by its type. Types are CamelCased.

        Refreshes once if the class is not found; subsequently, throws an
        error.
        """
        if obj_type not in cls.objects_dict:
            cls._refresh_registry()
        if obj_type not in cls.objects_dict:
            raise TypeError('\'%s\' is not a valid object class.' % obj_type)
        return cls.objects_dict[obj_type]


def get_default_object_values():
    """Returns a dictionary containing the default object values."""
    # TODO(wxy): Cache this as it is accessed many times.

    return json.loads(python_utils.get_package_file_contents(
        'extensions', feconf.OBJECT_DEFAULT_VALUES_EXTENSIONS_MODULE_PATH))
