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


# Field Configuration & Generator
class Field:
    def __init__(self, id, options):
        # '-1' means invalid field
        self.info = {
            "collection_id": -1,
            "parent_id": -1,
            "field_id": id,
            "cardinality": -1,
            "num_of_distinct": -1,
            "relationship": {},
            "children": [],
            "access_name": "field"+str(id),
            "parent": False,
            "find_count": 0,
            "update_count": 0,
            "condition_count": 0,
            "find_ratio": 0,
            "update_ratio": 0,
            "condition_ratio": 0,
            "totalnum": 0
        }
        self.info["type"] = random.choice(["int", "string"])
        self.data = {}
        self.options = options
        self.value = None
        self.operandset = ["$eq", "$gt", "$gte", "$ne", "$lt", "$lte"]
        self.result_keys = ["find_ratio", "update_ratio", "condition_ratio",
                            "cardinality", "parent_id", "collection_id",
                            "parent"]
        # Initialize
        for fid in range(self.options["num_of_fields_in_format"]):
            self.info["field"+str(fid)] = 0

    # Set Relationship
    def update_relationship(self, dicts):
        for fname, value in dicts.items():
            if fname not in self.info["relationship"]:
                self.info["relationship"][fname] = 0
            self.info["relationship"][fname] += value

    # Set Information
    def set_info(self, key, value):
        if self.info[key].__class__.__name__ == "list":
            if value is None:
                self.info[key] = []
            else:
                self.info[key].append(value)
        else:
            self.info[key] = value

    def get_info(self, key):
        return self.info[key]

    # Generate Value for field (considering cardinality)
    def generate_value(self):
        if self.info["type"] == "int":
            if self.info["num_of_distinct"] > 0:
                self.value = random.randrange(self.info["num_of_distinct"])
            else:
                self.value = 0
        elif self.info["type"] == "string":
            if self.info["num_of_distinct"] > 0:
                val = random.randrange(self.info["num_of_distinct"])
                self.value = str(val)
            else:
                self.value = "0"

    def generate_cond_value(self):
        value = None
        if self.info["type"] == "int":
            if self.info["num_of_distinct"] > 0:
                value = random.randrange(self.info["num_of_distinct"])
            else:
                value = 0
        elif self.info["type"] == "string":
            if self.info["num_of_distinct"] > 0:
                value = str(random.randrange(self.info["num_of_distinct"]))
            else:
                value = "0"
        return value

    def generate_cond_operand(self):
        operand = None
        if self.info["type"] == "int":
            operand = random.choice(self.operandset)
        elif self.info["type"] == "string":
            operand = "$eq"
        return operand

    def get_workload_info(self):
        buf = []
        keys = [
            "find_ratio",
            "update_ratio",
            "condition_ratio"]
        for key in keys:
            buf.append(self.info[key])
        return buf

    # Trick : Avoiding to use id(0), id is count up 1
    def get_structure_info(self):
        buf = []
        keys = [
            "collection_id",
            "parent_id",
            "parent",
            "cardinality"]
        for key in keys:
            value = self.info[key]
            if key == "parent_id" and value != -1:
                value = int(value.replace("field", "")) + 1
            elif key == "parent":
                value = int(value)
            elif key == "cardinality":
                value = int(value * 100)
            else:
                value = int(value) + 1
            buf.append(str(value))
        return buf

    def result(self):
        # print("> Result", "field", self.info["field_id"])
        for key in self.result_keys:
            if key == "cardinality":
                print(key, int(self.info[key]*100))
            elif key == "parent":
                print(key, int(self.info[key]))
            else:
                print(key, self.info[key])
        for i in range(self.options["num_of_fields_in_format"]):
            fname = "field" + str(i)
            if fname in self.info["relationship"]:
                ratio = self.info["relationship"][fname]
                ratio = ratio / self.info["totalnum"]
                print("relationship_"+fname, int(ratio * 100))
            else:
                print("relationship_"+fname, 0)

    # for Workload
    def reset_count(self):
        for key in ["find_count", "update_count", "condition_count"]:
            self.info[key] = 0
