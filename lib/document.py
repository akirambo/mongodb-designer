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
import operator
from lib import field as fg


class DocumentGenerator:
    def __init__(self, options):
        self.options = options
        self.fields = {}

    def exec(self):
        self.__create_fields()
        self.__create_cardinality()

    # create collections & parent field
    def create_structures(self):
        self.__reset_structures()
        # 1.Select Collection for Real Field
        num_of_fields = self.options["num_of_fields"]
        tmp = num_of_fields
        tmp = int(tmp / random.randrange(1, num_of_fields))
        fieldnum_col = tmp + 1
        array = range(num_of_fields)
        cols = [array[x:x + fieldnum_col] for x in range(0,
                                                         num_of_fields,
                                                         fieldnum_col)]
        self.options["num_of_collections"] = len(cols)
        # collection_id = -1 means an invalid field
        col_id = -1
        for collection in cols:
            col_id += 1
            for field_id in collection:
                # set collection_id
                fname = "field" + str(field_id)
                self.fields[fname].set_info("collection_id", col_id)
        # 2.Select Collection for Parent Field
        # create parent_fields
        max_parent_fields = self.options["num_of_fields_in_format"]
        max_parent_fields -= self.options["num_of_fields"]
        # Create Parent Field
        collection_num = len(cols)
        num_of_parent_fields = random.randint(0, max_parent_fields)
        parents_list = {}
        for i in range(0, collection_num):
            parents_list[i] = []

        for i in range(0, num_of_parent_fields):
            col_id = random.randint(0, collection_num - 1)
            fname = "field" + str(self.options["num_of_fields"] + i)
            self.fields[fname].set_info("collection_id", col_id)
            self.fields[fname].set_info("parent", True)
            parents_list[col_id].append("field"+str(field_id))
        # select children
        # Each parent field have at least one real field
        for collection_id, parents in parents_list.items():
            selected_parent_field = []
            if len(parents) > 0:
                for field_id in cols[collection_id]:
                    # select real field
                    parent_id = random.choice(parents)
                    selected_parent_field.append(parent_id)
                    fname = "field"+str(field_id)
                    self.fields[fname].set_info("parent_id", parent_id)
                    self.fields[fname].set_info("access_name", parent_id+"." + fname)
                    self.fields[parent_id].set_info("children", fname)
                    self.fields[parent_id].set_info("parent", True)
                    self.fields[parent_id].set_info("access_name", parent_id)

    def create_indexset(self):
        return self.__cardinality_indexset()
        # return self.__random_indexset()

    def __cardinality_indexset(self):
        indexs = []
        field2findratio = {}
        for fid, field in self.fields.items():
            field2findratio[fid] = field.get_info("find_ratio")
        sorted_find = sorted(field2findratio.items(),
                             key=operator.itemgetter(1))
        candidates = []
        for i in range(len(sorted_find)):
            target = sorted_find[-1]
            if target[1] > 25:
                candidates.append(target[0])
                del sorted_find[-1]
            else:
                break
        for i in range(len(candidates)):
            indexs.append(candidates[0:i])
        if len(indexs) == 0:
            indexs.append([])
        return indexs

    def __random_indexset(self):
        indexs = [[]]
        fields = list(self.fields.keys())
        for i in range(self.options["num_of_indexs"]):
            num_of_fields = random.randrange(len(fields))
            candidates = []
            for j in range(num_of_fields):
                f = random.choice(fields)
                if f not in candidates:
                    candidates.append(f)
            if candidates not in indexs:
                indexs.append(candidates)
        return indexs

    def __reset_structures(self):
        for fid, field in self.fields.items():
            field.set_info("access_name", fid)
            field.set_info("collection_id", -1)
            field.set_info("children", None)
            field.set_info("parent_id", -1)
            field.set_info("parent", False)

    def __create_fields(self):
        for i in range(0, self.options["num_of_fields_in_format"]):
            field = fg.Field(i, self.options)
            self.fields["field"+str(i)] = field

    # Field Cardinality select from
    #   [100:random, 75:25%, 50:50% of values are same, 75, 100:random]
    # cardinality == number of distinct / total number of documents
    def __create_cardinality(self):
        candidates = [0, 0.25, 0.5, 0.75, 1.0]
        for field in self.fields:
            cardinality = candidates[random.randrange(5)]
            num_of_dist = int(cardinality * self.options["num_of_documents"])
            self.fields[field].set_info("cardinality", cardinality)
            self.fields[field].set_info("num_of_distinct", num_of_dist)
