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

from pymongo import MongoClient


# Use pymongo version is 3.x
class QueryRunner:
    def __init__(self, options):
        self.options = options
        client = MongoClient(self.options["server"],
                             int(self.options["port"]))
        self.db = client[self.options["database"]]

    def reset(self, collection):
        self.db.drop_collection(collection)

    def insert_many(self, collection, docs):
        if self.options["norun"] is False:
            col = self.db[collection]
            col.insert_many(docs)
            # print("inserted for", collection, col.count({}))

    def information(self, collection):
        if self.options["norun"] is False:
            info = self.db.command('collstats', collection)
            return info
        else:
            return {"totalIndexSize": 0}

    def create_index(self, collection, field):
        if self.options["norun"] is False:
            col = self.db[collection]
            col.create_index(field)

    def drop_index(self, collection):
        if self.options["norun"] is False:
            col = self.db[collection]
            col.drop_indexes()

    def exec(self, collection, command, args):
        if self.options["norun"] is False:
            if command == "find":
                self.__find(collection, args)
            elif command == "update":
                self.__update(collection, args)

    def __find(self, collection, args):
        # print(collection, args)
        col = self.db[collection]
        col.find_one(args["condition"], args["projection"])

    def __update(self, collection, args):
        try:
            col = self.db[collection]
            # print(args["condition"], args["update"])
            col.update_one(args["condition"], args["update"])
        except ValueError:
            print("ERROR >", collection, args)
