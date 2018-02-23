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

import time
from lib import queryrunner as qr


class QueryExecuter:
    def __init__(self, options, fields, workloads):
        self.options = options
        self.queries = ["update", "find"]
        self.fields = fields
        self.collections = {}
        self.__build_collections()
        self.runner = qr.QueryRunner(options)
        self.workloads = workloads
        self.execution_time = 0.0
        self.server_info = {}
        self.index_fields = []

    def insert_init_documents(self):
        for cid, collection in self.collections.items():
            self.runner.reset("col"+str(cid))
            docs = []
            for i in range(self.options["num_of_documents"]):
                docs.append(self.__build_doc(collection))
                if len(docs) == self.options["upper_insert_many"]:
                    # run
                    self.runner.insert_many("col"+str(cid), docs)
                    docs = []
            if len(docs) > 0:
                # run
                self.runner.insert_many(docs)

    def create_index(self, fields):
        self.index_fields = fields
        for f in fields:
            for cid, fields in self.collections.items():
                if f in fields:
                    self.runner.create_index("col"+str(cid), f)
        self.__server_info()

    def drop_index(self, fields):
        self.index_fields = []
        for f in fields:
            for cid, fields in self.collections.items():
                self.runner.drop_index("col"+str(cid))

    def __server_info(self):
        info = {}
        for cid, collection in self.collections.items():
            info[cid] = self.runner.information("col"+str(cid))
        keys = ["totalIndexSize"]
        for key in keys:
            if key not in self.server_info:
                self.server_info[key] = 0
            for cid in self.collections:
                self.server_info[key] += info[cid][key]

    def run(self):
        starttime = time.time()
        for cname, queries in self.workloads.items():
            for command, qtypes in queries.items():
                for qtype in qtypes:
                    # print("query:", qtype.count, command, "@", cname)
                    for count in range(qtype.count):
                        qargs = qtype.generate(count)
                        self.runner.exec(cname, command, qargs)
        self.execution_time = time.time() - starttime

    # Get Dynamic Data
    def time(self):
        return self.execution_time

    # extract collection_id to field_ids
    def __build_collections(self):
        for cid in range(self.options["num_of_collections"]):
            self.collections[cid] = []
        for fid, field in self.fields.items():
            cid = field.get_info("collection_id")
            if not cid == -1:
                self.collections[cid].append(fid)

    def __build_doc(self, collection):
        doc = {}
        accessname2value = {}
        for fid in collection:
            access_name = self.fields[fid].get_info("access_name")
            if not self.fields[fid].get_info("parent"):
                self.fields[fid].generate_value()
                accessname2value[access_name] = self.fields[fid].value
        for aname, value in accessname2value.items():
            names = aname.split(".")
            self.__build_hierarchy(doc, names, value)
        return doc

    def __build_hierarchy(self, doc, names, value):
        name = names.pop(0)
        if name not in doc:
            doc[name] = {}
        if len(names) == 0:
            doc[name] = value
        else:
            self.__build_hierarchy(doc, names, value)
