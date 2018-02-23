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

import sys, os

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

from lib import optionparser as opt
from lib import workload as wg
from lib import document as doc
from lib import query as qg
from lib import tracer as tr
from lib import result as rs

if __name__ == '__main__':
    opts = opt.OptionParser()
    options = opts.exec()
    results = {}
    # Init outupt file
    if not os.path.exists(options["outdir"]):
        os.mkdir(options["outdir"])
    if os.path.exists(options["outdir"] + options["filename"]):
        os.remove(options["outdir"] + options["filename"])
    
    # Generate Documents (parameter)
    docs = doc.DocumentGenerator(options)
    docs.exec()
    fields = docs.fields
    # 1.Generate Workload (parameter)
    for wid in range(options["num_of_workloads"]):
        results[wid] = rs.Results(wid,
                                  options["num_of_fields_in_format"])
        w = wg.WorkloadGenerator(options, fields)
        w.exec()
        results[wid].set_workload(fields)
        # 2.Create Structures
        for str_id in range(options["num_of_structures"]):
            docs.create_structures()
            results[wid].append_structure(str_id, fields)
            indexset = docs.create_indexset()
            w.generate()
            workloads = w.get_workloads()
            q = qg.QueryExecuter(options, fields, workloads)
            # 3.Init Insert Documents (execute queries)
            q.insert_init_documents()
            for idx_id in range(len(indexset)):
                print("ID(workload, structure, index) =", wid, str_id, idx_id)
                results[wid].append_index(str_id, idx_id, indexset[idx_id])
                # print("Generate Training Data #" + str(idx_id))
                q.create_index(indexset[idx_id])
                # 4. Run Tracer
                qid = 0
                t = tr.Tracer(qid, options["norun"], options["tracer"])
                t.exec()
                # 5. Run Workload
                q.run()
                t.kill()
                t.convert()
                # Append Server Information
                results[wid].append_server_info(str_id, idx_id, q.server_info)
                # Append Execution Time
                results[wid].append_time(str_id, idx_id, q.time())
                # Output Info
                results[wid].output(options["outdir"] + options["filename"])
                # Reset
                q.drop_index(indexset[idx_id])
