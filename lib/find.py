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


class FindQuery:
    def __init__(self, count, project):
        self.project = self.__build(project)
        self.count = count
        self.conditions = {}
        # for each field
        self.cond_counts = {}
        self.fname2aname = {}

    def append_condition(self, fname, access_name, value, operand):
        data = {}
        data[access_name] = {}
        if fname not in self.fname2aname:
            self.fname2aname[fname] = access_name
            self.conditions[fname] = []
        data[access_name][operand] = value
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
            "projection": self.project
        }
        for ck, cv in self.cond_counts.items():
            if count < len(self.conditions[ck]):
                aname = self.fname2aname[ck]
                args["condition"][aname] = self.conditions[ck][count][aname]
        return args

    def get_relationships(self):
        relationships = {}
        # Projection
        for fname_ in self.project.keys():
            fname = fname_
            if "." in fname_:
                fname = fname_.split(".")[-1]
            # Conditions
            cond_count = 0
            if fname not in relationships:
                relationships[fname] = {}
            for cfname, conds in self.conditions.items():
                nocond_count = self.count - cond_count
                if cfname not in relationships[fname]:
                    relationships[fname][cfname] = 0
                if fname != cfname:
                    relationships[fname][cfname] += len(conds)
                # No Conditions
                relationships[fname][cfname] += nocond_count
        return relationships

    def __build(self, project):
        data = {}
        for p in project:
            data[p] = 1
        return data
