# imports
import multiprocessing
from distributed import Client
import os
import json
import time
import copy
from importlib.resources import files
import matplotlib.pyplot as plt
from ogeth.calibrate import Calibration
from ogcore.parameters import Specifications
from ogcore import output_tables as ot
from ogcore import output_plots as op
from ogcore.execute import runner
from ogcore.utils import safe_read_pickle
from ogeth.utils import is_connected
import ogcore

# Use a custom matplotlib style file for plots
plt.style.use("ogcore.OGcorePlots")


def main():
    # Define parameters to use for multiprocessing
    num_workers = min(multiprocessing.cpu_count(), 7)
    client = Client(n_workers=num_workers, threads_per_worker=1)
    print("Number of workers = ", num_workers)

    # Directories to save data
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    save_dir = os.path.join(CUR_DIR, "OG-ETH-Debt")
    base_dir = os.path.join(save_dir, "OUTPUT_BASELINE")
    image_dir = os.path.join(save_dir, "OG-ETH_Debt_plots")
    reform_tax_dir = os.path.join(save_dir, "OUTPUT_REFORM_Tax")
    reform_spend_dir = os.path.join(save_dir, "OUTPUT_REFORM_Spend")
    reform_grow_dir = os.path.join(save_dir, "OUTPUT_REFORM_Grow")

    # """
    # ---------------------------------------------------------------------------
    # Run baseline policy
    # ---------------------------------------------------------------------------
    # """
    # # Set up baseline parameterization
    # p = Specifications(
    #     baseline=True,
    #     num_workers=num_workers,
    #     baseline_dir=base_dir,
    #     output_base=base_dir,
    # )
    # # Update parameters for baseline from default json file
    # with (
    #     files("ogeth")
    #     .joinpath("ogeth_default_parameters.json")
    #     .open("r") as file
    # ):
    #     defaults = json.load(file)
    # p.update_specifications(defaults)
    # # Update parameters from calibrate.py Calibration class
    # if is_connected():  # only update if connected to internet
    #     c = Calibration(
    #         p, update_from_api=True
    #     )  # =True will update data from online sources
    #     updated_params = c.get_dict()
    #     p.update_specifications(updated_params)

    # # Update tax and spending parameters
    # updated_params = {
    #     "debt_ratio_ss": 0.75,
    # }
    # p.update_specifications(updated_params)

    # # Run model
    # start_time = time.time()
    # runner(p, time_path=True, client=client)
    # print("run time = ", time.time() - start_time)
    client.close()


    # """
    # ---------------------------------------------------------------------------
    # Run reform policy: increase CIT and IIT and consumption tax rates by 20%
    # ---------------------------------------------------------------------------
    # """

    # # Set up baseline parameterization
    # p2 = Specifications(
    #     baseline=False,
    #     num_workers=num_workers,
    #     baseline_dir=base_dir,
    #     output_base=reform_tax_dir,
    # )
    # # Update parameters for baseline from default json file
    # with (
    #     files("ogeth")
    #     .joinpath("ogeth_default_parameters.json")
    #     .open("r") as file
    # ):
    #     defaults = json.load(file)
    # p2.update_specifications(defaults)
    # # Update parameters from calibrate.py Calibration class
    # if is_connected():  # only update if connected to internet
    #     c = Calibration(
    #         p2, update_from_api=True
    #     )  # =True will update data from online sources
    #     updated_params = c.get_dict()
    #     p2.update_specifications(updated_params)

    # # p = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))

    # # # create new Specifications object for reform simulation
    # # p2 = copy.deepcopy(p)
    # # p2.baseline = False
    # # p2.output_base = reform_tax_dir

    # # # Update tax and spending parameters
    # # updated_params = {
    # #     "debt_ratio_ss": 0.55,
    # # }
    # # p.update_specifications(updated_params)

    # # Parameter change for the reform run
    # updated_params_tax = {
    #     "cit_rate": [[0.36]],  # decrease CIT rate to 25%
    #     "tau_c": [[0.084]],
    #     "etr_params": [[[0.036]]],
    #     "mtrx_params": [[[0.24]]],
    #     "mtry_params": [[[0.24]]],
    #     "debt_ratio_ss": 0.55,
    # }
    # p2.update_specifications(updated_params_tax)

    # # Run model
    # client = Client(n_workers=num_workers, threads_per_worker=1)
    # start_time = time.time()
    # runner(p2, time_path=True, client=client)
    # print("run time = ", time.time() - start_time)
    # client.close()

    # """
    # ---------------------------------------------------------------------------
    # Save some results, tax increase
    # ---------------------------------------------------------------------------
    # """
    # base_tpi = safe_read_pickle(os.path.join(base_dir, "TPI", "TPI_vars.pkl"))
    # base_params = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))
    # reform_tax_tpi = safe_read_pickle(
    #     os.path.join(reform_tax_dir, "TPI", "TPI_vars.pkl")
    # )
    # reform_tax_params = safe_read_pickle(
    #     os.path.join(reform_tax_dir, "model_params.pkl")
    # )
    # ans_tax = ot.macro_table(
    #     base_tpi,
    #     base_params,
    #     reform_tpi=reform_tax_tpi,
    #     reform_params=reform_tax_params,
    #     var_list=["Y", "C", "K", "L", "r", "w"],
    #     output_type="pct_diff",
    #     num_years=10,
    #     start_year=base_params.start_year,
    # )

    # # create plots of output
    # op.plot_all(
    #     base_dir,
    #     reform_tax_dir,
    #     os.path.join(reform_tax_dir, "plots_tables"),
    # )
    # # Create CSV file with output
    # ot.time_series_table(
    #     base_params,
    #     base_tpi,
    #     reform_tax_params,
    #     reform_tax_tpi,
    #     table_format="csv",
    #     path=os.path.join(
    #         reform_tax_dir, "plots_tables", "macro_time_series_output.csv"
    #     ),
    # )

    # print("Percentage changes in aggregates:", ans_tax)
    # # save percentage change output to csv file
    # ans_tax.to_csv(
    #     os.path.join(reform_tax_dir, "plots_tables", "output.csv")
    # )

    # """
    # ---------------------------------------------------------------------------
    # Run reform policy: decrease government spending alpha_G and alpha_T by 20%
    # ---------------------------------------------------------------------------
    # """

    # # # create new Specifications object for reform simulation
    # # p3 = copy.deepcopy(p)
    # # p3.baseline = False
    # # p3.output_base = reform_spend_dir

    # # Set up baseline parameterization
    # p3 = Specifications(
    #     baseline=False,
    #     num_workers=num_workers,
    #     baseline_dir=base_dir,
    #     output_base=reform_spend_dir,
    # )
    # # Update parameters for baseline from default json file
    # with (
    #     files("ogeth")
    #     .joinpath("ogeth_default_parameters.json")
    #     .open("r") as file
    # ):
    #     defaults = json.load(file)
    # p3.update_specifications(defaults)
    # # Update parameters from calibrate.py Calibration class
    # if is_connected():  # only update if connected to internet
    #     c = Calibration(
    #         p3, update_from_api=True
    #     )  # =True will update data from online sources
    #     updated_params = c.get_dict()
    #     p3.update_specifications(updated_params)

    # # p = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))

    # # # create new Specifications object for reform simulation
    # # p2 = copy.deepcopy(p)
    # # p2.baseline = False
    # # p2.output_base = reform_tax_dir

    # # # Update tax and spending parameters
    # # updated_params = {
    # #     "debt_ratio_ss": 0.55,
    # # }
    # # p.update_specifications(updated_params)

    # # Parameter change for the reform run
    # pct3 = 0.07
    # updated_params_spend = {
    #     "alpha_G": [0.095 * (1 - pct3)],
    #     "alpha_T": [0.05 * (1 - pct3)],
    #     "debt_ratio_ss": 0.55,
    # }
    # p3.update_specifications(updated_params_spend)

    # # Run model
    # client = Client(n_workers=num_workers, threads_per_worker=1)
    # start_time = time.time()
    # runner(p3, time_path=True, client=client)
    # print("run time = ", time.time() - start_time)
    # client.close()

    # """
    # ---------------------------------------------------------------------------
    # Save some results, spending decrease
    # ---------------------------------------------------------------------------
    # """
    # base_tpi = safe_read_pickle(os.path.join(base_dir, "TPI", "TPI_vars.pkl"))
    # base_params = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))
    # reform_spend_tpi = safe_read_pickle(
    #     os.path.join(reform_spend_dir, "TPI", "TPI_vars.pkl")
    # )
    # reform_spend_params = safe_read_pickle(
    #     os.path.join(reform_spend_dir, "model_params.pkl")
    # )
    # ans_spend = ot.macro_table(
    #     base_tpi,
    #     base_params,
    #     reform_tpi=reform_spend_tpi,
    #     reform_params=reform_spend_params,
    #     var_list=["Y", "C", "K", "L", "r", "w"],
    #     output_type="pct_diff",
    #     num_years=10,
    #     start_year=base_params.start_year,
    # )

    # # create plots of output
    # op.plot_all(
    #     base_dir,
    #     reform_spend_dir,
    #     os.path.join(reform_spend_dir, "plots_tables"),
    # )
    # # Create CSV file with output
    # ot.time_series_table(
    #     base_params,
    #     base_tpi,
    #     reform_spend_params,
    #     reform_spend_tpi,
    #     table_format="csv",
    #     path=os.path.join(
    #         reform_spend_dir, "plots_tables", "macro_time_series_output.csv"
    #     ),
    # )

    # print("Percentage changes in aggregates:", ans_spend)
    # # save percentage change output to csv file
    # ans_spend.to_csv(
    #     os.path.join(reform_spend_dir, "plots_tables", "output.csv")
    # )

    """
    ---------------------------------------------------------------------------
    Run reform policy: increase g_y productivity
    ---------------------------------------------------------------------------
    """

    # # create new Specifications object for reform simulation
    # p3 = copy.deepcopy(p)
    # p3.baseline = False
    # p3.output_base = reform_spend_dir

    # Set up baseline parameterization
    p4 = Specifications(
        baseline=False,
        num_workers=num_workers,
        baseline_dir=base_dir,
        output_base=reform_grow_dir,
    )
    # Update parameters for baseline from default json file
    with (
        files("ogeth")
        .joinpath("ogeth_default_parameters.json")
        .open("r") as file
    ):
        defaults = json.load(file)
    p4.update_specifications(defaults)
    # Update parameters from calibrate.py Calibration class
    if is_connected():  # only update if connected to internet
        c = Calibration(
            p4, update_from_api=True
        )  # =True will update data from online sources
        updated_params = c.get_dict()
        p4.update_specifications(updated_params)

    # p = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))

    # # create new Specifications object for reform simulation
    # p2 = copy.deepcopy(p)
    # p2.baseline = False
    # p2.output_base = reform_tax_dir

    # # Update tax and spending parameters
    # updated_params = {
    #     "debt_ratio_ss": 0.55,
    # }
    # p.update_specifications(updated_params)

    # Parameter change for the reform run
    pp4 = 0.022
    updated_params_grow = {
        "g_y_annual": 0.022489227511585136 + pp4,
        "debt_ratio_ss": 0.55,
    }
    p4.update_specifications(updated_params_grow)

    # Run model
    client = Client(n_workers=num_workers, threads_per_worker=1)
    start_time = time.time()
    runner(p4, time_path=True, client=client)
    print("run time = ", time.time() - start_time)
    client.close()

    """
    ---------------------------------------------------------------------------
    Save some results, spending decrease
    ---------------------------------------------------------------------------
    """
    base_tpi = safe_read_pickle(os.path.join(base_dir, "TPI", "TPI_vars.pkl"))
    base_params = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))
    reform_grow_tpi = safe_read_pickle(
        os.path.join(reform_grow_dir, "TPI", "TPI_vars.pkl")
    )
    reform_grow_params = safe_read_pickle(
        os.path.join(reform_grow_dir, "model_params.pkl")
    )
    ans_grow = ot.macro_table(
        base_tpi,
        base_params,
        reform_tpi=reform_grow_tpi,
        reform_params=reform_grow_params,
        var_list=["Y", "C", "K", "L", "r", "w"],
        output_type="pct_diff",
        num_years=10,
        start_year=base_params.start_year,
    )

    # create plots of output
    op.plot_all(
        base_dir,
        reform_grow_dir,
        os.path.join(reform_grow_dir, "plots_tables"),
    )
    # Create CSV file with output
    ot.time_series_table(
        base_params,
        base_tpi,
        reform_grow_params,
        reform_grow_tpi,
        table_format="csv",
        path=os.path.join(
            reform_spend_dir, "plots_tables", "macro_time_series_output.csv"
        ),
    )

    print("Percentage changes in aggregates:", ans_grow)
    # save percentage change output to csv file
    ans_grow.to_csv(
        os.path.join(reform_grow_dir, "plots_tables", "output.csv")
    )


if __name__ == "__main__":
    # execute only if run as a script
    main()
