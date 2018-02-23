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
from lib import find
from lib import update


class WorkloadGenerator:
    def __init__(self, options, fields):
        self.options = options
        self.queries = ["update", "find"]
        self.fields = fields
        self.workloads = []
        self.total_queires = 0

    def get_workloads(self):
        return self.workloads

    def get_total_queries(self):
        return self.total_queries

    def exec(self):
        # Create Ratio
        ratio = random.randrange(100)
        ratios = {
            "find": ratio,
            "update": 100 - ratio,
            "condition": random.randrange(100)
        }
        # print("RATIOS", ratios)
        for key in ["find", "update", "condition"]:
            num_of_count = int(self.options["num_of_queries"]*ratios[key]/100)
            fields = list(self.fields.keys())
            if key == "condition":
                for n, f in self.fields.items():
                    if f.get_info("parent") is True:
                        fields.remove(n)
            for field in self.fields.values():
                if field not in fields:
                    if num_of_count == 0:
                        count = 0
                    else:
                        count = random.randrange(num_of_count)
                    field.set_info(key+"_count", count)
                    ratio = int(count / self.options["num_of_queries"] * 100)
                    field.set_info(key+"_ratio", ratio)

    def generate(self):
        collections = self.__collections_list()
        queries = {}
        totalnum = self.__get_totalnum_queries(collections)
        for cname, fields in collections.items():
            queries_ = {"find": {}, "update": {}}
            # generate find
            queries_["find"] = self.__generate_find(fields)
            # generate update
            queries_["update"] = self.__generate_update(fields)
            # generate condition
            self.__generate_condition(fields, queries_)
            queries[cname] = queries_
            self.__build_relationships(queries_, totalnum)
        self.workloads = queries

    def __get_totalnum_queries(self, collections):
        count = 0
        for cname, fields in collections.items():
            for fname in fields:
                for key in ["find", "update"]:
                    count += self.fields[fname].get_info(key + "_count")
        return count

    def __build_relationships(self, queries, totalnum):
        for qtype, qs in queries.items():
            for q in qs:
                info = q.get_relationships()
                if info is not None:
                    for fname, dicts in info.items():
                        self.fields[fname].update_relationship(dicts)
                        self.fields[fname].set_info("totalnum", totalnum)

    def __collections_list(self):
        collections = {}
        for fid, field in self.fields.items():
            cid = str(field.get_info("collection_id"))
            if field.get_info("parent") is not True and cid != "-1":
                cname = "col" + cid
                if cname not in collections:
                    collections[cname] = []
                collections[cname].append(fid)
        return collections

    def __generate_find(self, fields):
        counts = {}
        max = 0
        for fname in fields:
            counts[fname] = self.fields[fname].get_info("find_count")
            if max < counts[fname]:
                max = counts[fname]
        finds = []
        while max > 0:
            min = -1
            # get min operation count
            for fname in counts:
                if counts[fname] != 0:
                    if min == -1 or min > counts[fname]:
                        min = counts[fname]
            project_fields = []
            for fname in counts.keys():
                # print(fname, counts[fname])
                if counts[fname] != 0:
                    counts[fname] -= min
                    access_name = self.fields[fname].get_info("access_name")
                    project_fields.append(access_name)
                    query = find.FindQuery(min, project_fields)
                    finds.append(query)
            max -= min
        return finds

    def __generate_update(self, fields):
        updates = []
        for fname in fields:
            count = self.fields[fname].get_info("update_count")
            access_name = self.fields[fname].get_info("access_name")
            value_type = self.fields[fname].get_info("type")
            distinct = self.fields[fname].get_info("num_of_distinct")
            updates.append(update.UpdateQuery(count, access_name,
                                              value_type, distinct))
        return updates

    def __generate_condition(self, fields, queries):
        for fname in fields:
            count = self.fields[fname].get_info("condition_count")
            access_name = self.fields[fname].get_info("access_name")
            candidates = {}
            if self.fields[fname].get_info("parent"):
                next
            for name, query in queries.items():
                id = 0
                for q in query:
                    no_cond_count = q.no_condition_count(fname)
                    if no_cond_count > 0:
                        candidates[name+"_"+str(id)] = no_cond_count
                    id += 1

            for i in range(count):
                if len(list(candidates.keys())) > 0:
                    name = random.choice(list(candidates.keys()))
                    # q[0] = query_type, q[1] = index
                    q = name.split("_")
                    value = self.fields[fname].generate_cond_value()
                    operand = self.fields[fname].generate_cond_operand()
                    queries[q[0]][int(q[1])].append_condition(fname,
                                                              access_name,
                                                              value,
                                                              operand)
                    candidates[name] -= 1
                    if candidates[name] == 0:
                        del candidates[name]
