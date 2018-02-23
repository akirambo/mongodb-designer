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


class Structure:
    def __init__(self, str_id, fields, num_of_fields):
        self.structure_id = str_id
        self.structures = {}
        self.workloads = {}
        self.indexs = {}
        self.num_of_fields = num_of_fields
        self.times = {}
        self.server_info = {}
        self.headers = [
            "collection_id", "parent_id", "parent", "cardinality",
            "index"
        ]
        for fid in range(num_of_fields):
            fname = "field" + str(fid)
            if fname in fields:
                self.structures[fname] = fields[fname].get_structure_info()
                self.workloads[fname] = fields[fname].get_workload_info()

    def append_index(self, index_id, indexset):
        self.indexs[index_id] = indexset

    def append_server_info(self, index_id, info):
        self.server_info[index_id] = info

    def append_time(self, index_id, time):
        self.times[index_id] = str(time)

    def output_bestmodel(self, index_id):
        structure = self.__output_struct()
        index = self.__output_index(index_id)
        return structure + index

    def output(self, withtime):
        buf = []
        structure = self.__output_struct()
        workload = self.__output_workload()
        if len(self.indexs.keys()) > 0:
            # Indexed
            for index_id in self.indexs.keys():
                index = self.__output_index(index_id)
                val = structure + workload + index
                if withtime is True:
                    val.append(self.times[index_id])
                buf.append(val)
        else:
            # No indexed
            index = self.__output_index(-1)
            val = structure + workload + index
            if withtime is True:
                val.append(self.times[index_id])
            buf.append(val)
        return buf

    def __output_struct(self):
        buf = []
        for fid in range(self.num_of_fields):
            fname = "field" + str(fid)
            # [collection_id, parent_id, parent, cardinality] for each field
            buf.extend(self.structures[fname])
        return buf

    def __output_workload(self):
        buf = []
        for fid in range(self.num_of_fields):
            fname = "field" + str(fid)
            # [find_ratio, update_ratio, condition_ratio]
            buf.extend(self.workloads[fname])
        return buf

    def __output_index(self, index_id):
        buf = []
        for fid in range(self.num_of_fields):
            value = 0
            fname = "field" + str(fid)
            if index_id != -1 and index_id in self.indexs:
                if fname in self.indexs[index_id]:
                    value = 1
            buf.append(str(value))
        return buf
