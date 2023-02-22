"""Available statistical tests.
For detailed information about statistical tests see module documentation.
"""
from .anderson_darling_stattest import anderson_darling_test
from .chisquare_stattest import chi_stat_test
from .cramer_von_mises_stattest import cramer_von_mises
from .energy_distance import energy_dist_test
from .epps_singleton_stattest import epps_singleton_test
from .fisher_exact_stattest import fisher_exact_test
from .g_stattest import g_test
from .hellinger_distance import hellinger_stat_test
from .jensenshannon import jensenshannon_stat_test
from .kl_div import kl_div_stat_test
from .ks_stattest import ks_stat_test
from .mann_whitney_urank_stattest import mann_whitney_u_stat_test
from .mmd_stattest import emperical_mmd
from .psi import psi_stat_test
from .registry import PossibleStatTestType
from .registry import StatTest
from .registry import StatTestFuncType
from .registry import get_stattest
from .registry import register_stattest
from .t_test import t_test
from .text_content_drift import text_content_drift_stat_test
from .tvd_stattest import tvd_test
from .wasserstein_distance_norm import wasserstein_stat_test
from .z_stattest import z_stat_test
