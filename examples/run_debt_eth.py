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
    reform_tax_dir = os.path.join(save_dir, "OUTPUT_REFORM_Tax")
    reform_spend_dir = os.path.join(save_dir, "OUTPUT_REFORM_Spend")
    reform_grow_dir = os.path.join(save_dir, "OUTPUT_REFORM_Grow")

    """
    ---------------------------------------------------------------------------
    Run baseline policy
    ---------------------------------------------------------------------------
    """
    # Set up baseline parameterization
    p = Specifications(
        baseline=True,
        num_workers=num_workers,
        baseline_dir=base_dir,
        output_base=base_dir,
    )
    # Update parameters for baseline from default json file
    # with (
    #     files("ogeth")
    #     .joinpath("ogeth_default_parameters.json")
    #     .open("r") as file
    # ):
    with (
        files("ogeth")
        .joinpath("ogeth_default_parameters.json")
        .open("r") as file
    ):
        defaults = json.load(file)
    p.update_specifications(defaults)
    # Update parameters from calibrate.py Calibration class
    if is_connected():  # only update if connected to internet
        c = Calibration(
            p, update_from_api=True
        )  # =True will update data from online sources
        updated_params = c.get_dict()
        p.update_specifications(updated_params)

    # # Update tax and spending parameters
    # updated_params = {
    #     "alpha_T": [0.33],
    #     "alpha_G": [0.27],
    #     "cit_rate": [[0.28]],
    #     "tau_c": [[0.16]],
    #     "tau_payroll": [0.16],
    #     "etr_params": [[[0.03]]],
    #     "mtrx_params": [[[0.20]]],
    #     "mtry_params": [[[0.20]]],
    # }
    # p.update_specifications(updated_params)

    # Run model
    start_time = time.time()
    runner(p, time_path=True, client=client)
    print("run time = ", time.time() - start_time)

    plt.plot()

    # """
    # ---------------------------------------------------------------------------
    # Run reform policy
    # ---------------------------------------------------------------------------
    # """

    # # create new Specifications object for reform simulation
    # p2 = copy.deepcopy(p)
    # p2.baseline = False
    # p2.output_base = reform_dir

    # # Parameter change for the reform run
    # updated_params_ref = {
    #     "cit_rate": [[0.25]],  # decrease CIT rate to 25%
    # }
    # p2.update_specifications(updated_params_ref)

    # # Run model
    # start_time = time.time()
    # runner(p2, time_path=True, client=client)
    # print("run time = ", time.time() - start_time)
    # client.close()

    """
    ---------------------------------------------------------------------------
    Save some results of simulations
    ---------------------------------------------------------------------------
    """
    base_tpi = safe_read_pickle(os.path.join(base_dir, "TPI", "TPI_vars.pkl"))
    base_params = safe_read_pickle(os.path.join(base_dir, "model_params.pkl"))

    # Plot Debt-to-GDP ratio time path
    plot_path = (
        "/Users/richardevans/Docs/Economics/OSE/OG/OG-Core/examples/" +
        "OG-Core-Example/OG-Core_example_plots/DebtGDPratioBase.png"
    )
    op.plot_gdp_ratio(
        base_tpi,
        base_params,
        reform_tpi=None,
        reform_params=None,
        var_list=["D"],
        plot_type="levels",
        num_years_to_plot=75,
        start_year=base_params.start_year,
        vertical_line_years=base_params.T1,
        plot_title="Debt-to-GDP baseline: 2026-2100",
        path=None,
    )
    # reform_tpi = safe_read_pickle(
    #     os.path.join(reform_dir, "TPI", "TPI_vars.pkl")
    # )
    # reform_params = safe_read_pickle(
    #     os.path.join(reform_dir, "model_params.pkl")
    # )
    # ans = ot.macro_table(
    #     base_tpi,
    #     base_params,
    #     reform_tpi=reform_tpi,
    #     reform_params=reform_params,
    #     var_list=["Y", "C", "K", "L", "r", "w"],
    #     output_type="pct_diff",
    #     num_years=10,
    #     start_year=base_params.start_year,
    # )

    # # create plots of output
    # op.plot_all(
    #     base_dir, reform_dir, os.path.join(save_dir, "OG-ETH_example_plots")
    # )

    # print("Percentage changes in aggregates:", ans)
    # # save percentage change output to csv file
    # ans.to_csv(os.path.join(save_dir, "OG-ETH_example_output.csv"))


if __name__ == "__main__":
    # execute only if run as a script
    main()
