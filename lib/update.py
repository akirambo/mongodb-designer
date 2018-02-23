#
# Copyright (c) 2018, Carnegie Mellon University.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import random


class UpdateQuery:
    def __init__(self, count, field, value_type, num_of_distinct):
        self.field = field
        self.count = count
        self.value_type = value_type
        self.num_of_distinct = num_of_distinct
        self.conditions = {}
        # for each field
        self.cond_counts = {}
        self.fname2aname = {}

    def append_condition(self, fname, access_name, value, operand):
        data = {}
        data[access_name] = {}
        data[access_name][operand] = value
        if fname not in self.conditions:
            self.conditions[fname] = []
            self.fname2aname[fname] = access_name

        self.conditions[fname].append(data)
        if fname not in self.cond_counts:
            self.cond_counts[fname] = 0
        self.cond_counts[fname] += 1

    def no_condition_count(self, fname):
        if fname in self.cond_counts:
            return self.count - self.cond_counts[fname]
        return self.count

    def generate(self, count):
        args = {
            "condition": {},
            "update": {"$set": self.field}
        }
        args["update"]["$set"] = {self.field: self.__rand_value()}
        for ck, cv in self.cond_counts.items():
            if count < len(self.conditions[ck]):
                name = self.fname2aname[ck]
                value = self.conditions[ck][count][self.fname2aname[ck]]
                args["condition"][name] = value
        return args

    def __rand_value(self):
        value = None
        if self.value_type == "int":
            if self.num_of_distinct > 0:
                value = random.randrange(self.num_of_distinct)
            else:
                value = 0
        elif self.value_type == "string":
            if self.num_of_distinct > 0:
                value = str(random.randrange(self.num_of_distinct))
            else:
                value = "0"
        return value

    def get_relationships(self):
        relationships = {}
        fname = self.field
        if "." in self.field:
            fname = self.field.split(".")[-1]
        if fname not in relationships:
            relationships[fname] = {}
        for name, conds in self.conditions.items():
            if name not in relationships[fname]:
                relationships[fname][name] = 0
            relationships[fname][name] += len(conds)
        return relationships
