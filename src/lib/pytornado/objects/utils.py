#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2017-2019 Airinnova AB and the PyTornado authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Authors:
# * Alessandro Gastaldi
# * Aaron Dettmann

"""
Miscellaneous data structures for PyTornado.

Developed for Airinnova AB, Stockholm, Sweden.
"""


from collections import OrderedDict, MutableMapping


class FixedNamespace(object):
    """
    Immutable SIMPLENAMESPACE variant.

    Functions as a RECORD- or STRUCT-like object.
    Attributes of FIXEDNAMESPACE are accessed by dot notation: 'name.attr'.

    __MUTABLE controls how attributes are created and modified:

        * When TRUE, assigning a value to an undefined attribute creates it.
        * When FALSE, this instead raises an AttributeError.

    __MUTABLE is TRUE by default. _FREEZE sets __MUTABLE to FALSE.

    [1] https://docs.python.org/3.5/library/types.html
    """

    __mutable = True

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __setattr__(self, key, value):
        if not self.__mutable and not hasattr(self, key):
            raise AttributeError(f"Immutable instance of FixedNamespace does not have attribute '{key}'.")

        object.__setattr__(self, key, value)

    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}:\n ( {} )".format(type(self).__name__, ",\n ".join(items))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def _freeze(self):
        """Make current instance of FIXEDNAMESPACE immutable."""

        self.__mutable = False

    def _unfreeze(self):
        """Make current instance of FIXEDNAMESPACE mutable."""

        self.__mutable = True


class FixedOrderedDict(MutableMapping):
    """
    Immutable ORDEREDDICT[1] variant, based on MUTABLEMAPPING[2].

    Works as a dictionary with ordered key-value pairs.
    Entries of FIXEDORDEREDDICT are accessed by key: 'obj[key]'.

    __MUTABLE controls how key-value pairs are created and modified:
    * When TRUE, assigning a value to an undefined key creates a new entry.
    * When FALSE, this instead raises an KeyError.

    __MUTABLE is TRUE by default. _FREEZE sets __MUTABLE to FALSE.

    [1] collections.OrderedDict
    [2] collections.MutableMapping
    """

    __mutable = True

    def __init__(self, *args):
        self._dictionary = OrderedDict(*args)

    def __getitem__(self, key):
        return self._dictionary[key]

    def __setitem__(self, key, value):
        if not self.__mutable and key not in self._dictionary:
            raise KeyError(f"Instance of FixedOrderedDict does not have item '{key}'.")

        self._dictionary[key] = value

    def __delitem__(self, key):
        raise NotImplementedError("Cannot delete item of instance of FixedOrderedDict.")

    def __iter__(self):
        return iter(self._dictionary)

    def __repr__(self):
        items = ("{}={!r}".format(k, v) for k, v in self._dictionary.items())
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __len__(self):
        return len(self._dictionary)

    def _freeze(self):
        """Add item to instance of FIXEDORDEREDDICT, with DEFAULT value."""

        self.__mutable = False


class CaseDefinitionError(Exception):
    """Raised when insufficient data is provided for selected analysis."""

    pass