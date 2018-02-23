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

import csv
from lib import structure as st


class Results:
    def __init__(self, wid, num_of_fields):
        self.wid = wid
        # in format
        self.num_of_fields = num_of_fields
        self.workload = {}
        # structure_id => {fields => data}
        self.structures = {}
        self.indexs = {}
        self.times = {}
        self.besttime = 0
        self.besttime_ids = {
            "structure_id": 0,
            "index_id": 0
        }

    def set_workload(self, fields):
        # print("find_ratio, update_ratio, condition_ratio")
        for fid in range(self.num_of_fields):
            fname = "field" + str(fid)
            # print("Workload information >", fname)
            if fname in fields:
                self.workload[fname] = fields[fname].get_workload_info()
                # print(fname, fields[fname].get_workload_info())

    def append_structure(self, str_id, fields):
        self.structures[str_id] = st.Structure(str_id,
                                               fields,
                                               self.num_of_fields)

    def append_index(self, str_id, index_id, indexset):
        self.structures[str_id].append_index(index_id,
                                             indexset)

    def append_time(self, str_id, index_id, exectime):
        print("append time", exectime)
        if str_id not in self.times:
            self.times[str_id] = {}
        self.times[str_id][index_id] = exectime
        self.structures[str_id].append_time(index_id, exectime)
        if self.besttime == 0 or (self.besttime > exectime):
            self.besttime = exectime
            self.besttime_ids["structure_id"] = str_id
            self.besttime_ids["index_id"] = index_id
        print("besttime", self.besttime_ids, self.besttime)

    def append_relationships(self, str_id, index_id, fields):
        for fid in range(self.num_of_fields_in_format):
            fname = "field" + str(fid)
            if fname in self.fields:
                self.fields["field" + str(fid)].result()

    def append_server_info(self, str_id, index_id, info):
        self.structures[str_id].append_server_info(index_id, info)


#    def output(self, filename):
#        best = self.__output_bestmodel()
#        with open(filename, 'a', newline='') as csvfile:
#            csvwriter = csv.writer(csvfile, delimiter=',')
#            for str_id, structure in self.structures.items():
#                structures = structure.output(False)
#                for st in structures:
#                    csvwriter.writerow(st + best)
    
    def output(self, filename):
        best = self.__output_bestmodel()
        with open(filename, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            for str_id, structure in self.structures.items():
                structures = structure.output(True)
                for st in structures:
                    csvwriter.writerow(st + best)

    def __output_bestmodel(self):
        str_id = self.besttime_ids["structure_id"]
        index_id = self.besttime_ids["index_id"]
        return self.structures[str_id].output_bestmodel(index_id)
