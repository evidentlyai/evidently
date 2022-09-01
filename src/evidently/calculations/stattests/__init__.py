#!/usr/bin/env python
# coding: utf-8
from .ks_stattest import ks_stat_test
from .z_stattest import z_stat_test
from .chisquare_stattest import chi_stat_test
from .jensenshannon import jensenshannon_stat_test
from .kl_div import kl_div_stat_test
from .psi import psi_stat_test
from .wasserstein_distance_norm import wasserstein_stat_test
from .registry import get_stattest, register_stattest, StatTest, PossibleStatTestType, StatTestFuncType
