import math
import os
import time
import random
from exps.shared_args import parse_arguments
import calendar


def run_one_fixed_budget_alg(sh, time_per_epoch):
    # calculate min time required for evaluating 500 models
    min_epoch_for_fixed_k = sh.pre_calculate_epoch_required(total_models, 1)
    min_time_for_fixed_k = math.ceil(time_per_epoch * min_epoch_for_fixed_k)

    if sh.name == "SUCCREJCT":
        fully_train_each_model = int(244336900 / 500 * total_models)
        step = int((fully_train_each_model - min_time_for_fixed_k) / 30)
    else:
        fully_train_each_model = math.floor(total_models * 200 * time_per_epoch)
        step = int((fully_train_each_model - min_time_for_fixed_k) / 30)

    acc_reached = []
    time_used = []

    for run_id in range(total_run):
        begin_time = time.time()
        acc_each_run = []
        time_each_run = []
        for time_budget_used in range(min_time_for_fixed_k, fully_train_each_model, step):
            begin_time_u = time.time()
            U = sh.schedule_budget_per_model_based_on_T(args.search_space, time_budget_used, total_models)
            end_time_u = time.time()
            # print(f"run_id = {run_id}, time_usage for U = {end_time_u - begin_time_u}")

            begin_time_u = time.time()
            best_arch, _, B2_actual_epoch_use = sh.run_phase2(U, all_models[run_id])
            end_time_u = time.time()
            # print(f"run_id = {run_id}, time_usage for run = {end_time_u - begin_time_u}")

            begin_time_u = time.time()
            acc_sh_v, _ = fgt.get_ground_truth(arch_id=best_arch, dataset=args.dataset, epoch_num=None)
            end_time_u = time.time()
            # print(f"run_id = {run_id}, get ground truth for run = {end_time_u - begin_time_u}")

            acc_each_run.append(acc_sh_v)
            time_each_run.append(B2_actual_epoch_use / 60)
            print(
                f" *********** begin with U={U}, K={len(all_models[run_id])}, "
                f"B2_actual_epoch_use = {B2_actual_epoch_use}, acc = {acc_sh_v}, "
                f"fully_train_each_model = {fully_train_each_model}, ***********")
        end_time = time.time()
        print(f"run_id = {run_id}, time_usage = {end_time - begin_time}")

        acc_reached.append(acc_each_run)
        time_used.append(time_each_run)

    return acc_reached, time_used


if __name__ == "__main__":

    args = parse_arguments()

    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    os.environ.setdefault("log_logger_folder_name", f"{args.log_folder}")
    os.environ.setdefault("log_file_name", args.log_name + "_" + str(ts) + ".log")
    os.environ.setdefault("base_dir", args.base_dir)

    from src.query_api.interface import SimulateTrain
    from src.query_api.query_api_img import guess_train_one_epoch_time
    from src.eva_engine.phase2.evaluator import P2Evaluator
    from src.eva_engine.phase2.run_sh import BudgetAwareControllerSH
    from src.eva_engine.phase2.run_sr import BudgetAwareControllerSR
    from src.eva_engine.phase2.run_uniform import UniformAllocation
    from src.search_space.nas_201_api.model_params import NB201MacroCfg
    from src.search_space.nas_201_api.space import NasBench201Space
    from src.tools.io_tools import write_json

    total_run = 3
    total_models = 500

    # sample 100 * 500 models,
    all_models = []
    for run_id in range(total_run):
        _models = random.sample(list(range(1, 15624)), total_models)
        all_models.append(_models)

    model_cfg = NB201MacroCfg(None, None, None, None, None)
    space_ins = NasBench201Space(None, model_cfg)
    train_time_per_epoch = guess_train_one_epoch_time(args.search_space, args.dataset)
    fgt = SimulateTrain(space_name=args.search_space)
    evaluator = P2Evaluator(search_space_ins=space_ins,
                            dataset=args.dataset,
                            is_simulate=True)

    result_save_dic = {}

    print("--- benchmarking sh_")
    sh_ = BudgetAwareControllerSH(search_space_ins=space_ins,
                                  dataset_name=args.dataset,
                                  eta=3, time_per_epoch=train_time_per_epoch,
                                  args=args)
    acc_reached, time_used = run_one_fixed_budget_alg(sh_, train_time_per_epoch)
    result_save_dic["sh"] = {"time_used": time_used, "acc_reached": acc_reached}

    print("--- benchmarking uniform_")
    uniform_ = UniformAllocation(evaluator=evaluator,
                                 time_per_epoch=train_time_per_epoch)
    acc_reached, time_used = run_one_fixed_budget_alg(uniform_, train_time_per_epoch)
    result_save_dic["uniform"] = {"time_used": time_used, "acc_reached": acc_reached}

    print("--- benchmarking sr_")
    sr_ = BudgetAwareControllerSR(evaluator=evaluator,
                                  time_per_epoch=train_time_per_epoch)
    acc_reached, time_used = run_one_fixed_budget_alg(sr_, train_time_per_epoch)
    result_save_dic["sr"] = {"time_used": time_used, "acc_reached": acc_reached}

    write_json(f"{args.result_dir}/micro_phase2_{args.dataset}", result_save_dic)
