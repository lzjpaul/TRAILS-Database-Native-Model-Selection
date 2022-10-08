from common.constant import *
from eva_engine.phase1.grad_norm import GradNormEvaluator
from eva_engine.phase1.grad_plain import GradPlainEvaluator
from eva_engine.phase1.nas_wot import NWTEvaluator
from eva_engine.phase1.ntk_condition_num import NTKCondNumEvaluator
from eva_engine.phase1.ntk_trace import NTKTraceEvaluator
from eva_engine.phase1.ntk_trace_approx import NTKTraceApproxEvaluator
from eva_engine.phase1.prune_fisher import FisherEvaluator
from eva_engine.phase1.prune_grasp import GraspEvaluator
from eva_engine.phase1.prune_snip import SnipEvaluator
from eva_engine.phase1.prune_synflow import SynFlowEvaluator
from eva_engine.phase1.weight_norm import WeightNormEvaluator

# evaluator mapper to register many existing evaluation algorithms
evaluator_register = {

    # # sum on gradient
    CommonVars.GRAD_NORM: GradNormEvaluator(),
    CommonVars.GRAD_PLAIN: GradPlainEvaluator(),
    #
    # # training free matrix
    # CommonVars.JACOB_CONV: JacobConvEvaluator(),
    CommonVars.NAS_WOT: NWTEvaluator(),

    # this is ntk based
    CommonVars.NTK_CONDNUM: NTKCondNumEvaluator(),
    CommonVars.NTK_TRACE: NTKTraceEvaluator(),

    CommonVars.NTK_TRACE_APPROX: NTKTraceApproxEvaluator(),

    # # prune based
    CommonVars.PRUNE_FISHER: FisherEvaluator(),
    CommonVars.PRUNE_GRASP: GraspEvaluator(),
    CommonVars.PRUNE_SNIP: SnipEvaluator(),
    CommonVars.PRUNE_SYNFLOW: SynFlowEvaluator(),

    # # sum of weight
    CommonVars.WEIGHT_NORM: WeightNormEvaluator(),

}
