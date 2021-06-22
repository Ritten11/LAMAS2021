from View.ModelServer import ModelServer
from ResistanceModel.ResistanceModel import ResistanceModel
from mesa.batchrunner import BatchRunner, BatchRunnerMP
import argparse
import os
import errno


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
    parser.add_argument('-iter', '--iterations', default=10, type=int, choices=range(1, 200),
                        help='Specify the number of iterations for each condition')
    return parser


parser = init_argparse()
options = parser.parse_args()
args = vars(options)
# grid = CanvasGrid(agent_portrayal, 24, 9, 1000, 500)
#


def get_identity_revealed(model):
    return model.identity_revealed


def get_mission_results(model):  # transform the bit-array into the corresponding integer.
    return 16*model.rounds_won_spies[0] + \
           8*model.rounds_won_spies[1] + \
           4*model.rounds_won_spies[2] + \
           2*model.rounds_won_spies[3] + \
           model.rounds_won_spies[4]

if options.run_mode == 'gui':
    server = ModelServer(N=options.number_of_agents, ps=options.party_size, hok=options.higher_order_knowledge)

    server.run_server()
elif options.run_mode == 'batch':
    fixed_params = {"N": 5,
                    "S": 2,
                    "height": 5,
                    "width": 7}
    variable_params = {"ps": ['2', 'default', '3'],
                       "hok": [True, False]}

    batch_run = BatchRunner(ResistanceModel,
                            variable_params,
                            fixed_params,
                            iterations=options.iterations,
                            max_steps=50,
                            model_reporters={"rounds_won_spies": get_mission_results,
                                             "identity_revealed": get_identity_revealed})
    batch_run.run_all()
    run_data = batch_run.get_model_vars_dataframe()
    print(f"levels rounds_won: {run_data['rounds_won_spies'].unique()}")
    print(f"levels identity_revealed: {run_data['identity_revealed'].unique()}")
    print(f"levels higher order knowledge: {run_data['hok'].unique()}")
    print(f"levels ps: {run_data['ps'].unique()}")
    print(f"levels N: {run_data['N'].unique()}")
    try:
        os.mkdir("results")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with open('results' + os.path.sep + 'output_' + str(options.number_of_agents) + '.json', 'w') as outfile:
        run_data.to_json(outfile)
else:
    print("Please pick a valid option for the --run_mode flag")
# server = ModelServer()
#
# server.run_server()

