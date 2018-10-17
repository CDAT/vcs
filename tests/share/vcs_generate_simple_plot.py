#!/usr/bin/env python
import vcs
x = vcs.init(bg=True)
x.plot([1,2,3,2,1,4,5,2,1,4])
x.png("test_vcs_generate_simple_plot", provenance=True)