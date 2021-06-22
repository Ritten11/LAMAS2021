from View.ModelServer import ModelServer
from ResistanceModel.ResistanceModel import ResistanceModel
from mesa.batchrunner import BatchRunner, BatchRunnerMP
import argparse
import os


def init_argparse() -> argparse.ArgumentParser:
    """Initialise the command line argument parser.
    Returns:
        argparse.ArgumentParser: The argument parser
    """
    parser = argparse.ArgumentParser(
        description="Run a simulation of the Resistance game")
    parser.add_argument('-N', '--number_of_agents', default=5, type=int,
                        choices=[5, 6],
                        help="Set the number of agents within the simulation"),
    parser.add_argument('-rm', '--run_mode', default='gui', type=str,
                        choices=['gui', 'batch'],
                        help="Specify what mode you want to run the simulation in")
    parser.add_argument('-ps', '--party_size', default='default', type=str,
                        choices=['2', 'default', '3'],
                        help="Specify how big the mission parties should be")
    parser.add_argument('-hok', '--higher_order_knowledge', default=False, type=bool,
                        help="Specify whether the spies should use higher order knowledge")
    parser.add_argument('-iter', '--iterations', default=100, type=int, choices=range(1, 100),
                        help='Specify the number of iterations for each condition')
    return parser


parser = init_argparse()
options = parser.parse_args()
args = vars(options)
# grid = CanvasGrid(agent_portrayal, 24, 9, 1000, 500)
#

if options.run_mode == 'gui':
    server = ModelServer(N=options.number_of_agents, ps=options.party_size, hok=options.higher_order_knowledge)

    server.run_server()
elif options.run_mode == 'batch':
    fixed_params = {"N": 5}
    variable_params = {"ps": ['2', 'default', '3'],
                       "hok": [True, False]}

    batch_run = BatchRunner(ResistanceModel,
                            variable_params,
                            fixed_params,
                            iterations=options.iterations,
                            max_steps=50,
                            model_reporters={"Rounds_won_spies": "total_t",
                                             "Number_of_rounds": "total_sd"})
    batch_run.run_all()
    run_data = batch_run.get_agent_vars_dataframe()
    print(f"levels sd: {run_data['social_distance'].unique()}")
    print(f"levels sm: {run_data['seat_mode'].unique()}")
    print(f"levels vent: {run_data['vent'].unique()}")
    print(f"levels one_way: {run_data['one_way'].unique()}")
    try:
        os.mkdir("results")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with open('results' + os.path.sep + 'output_' + options.occupancy + '.json', 'w') as outfile:
        run_data.to_json(outfile)
else:
    print("Please pick a valid option for the --run_mode flag")
# server = ModelServer()
#
# server.run_server()

