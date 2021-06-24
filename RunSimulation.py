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
                        choices=['2', 'def', '3'],
                        help="Specify how big the mission parties should be. \
                             Use the default for the original game settings")
    parser.add_argument('-sphok', '--spies_higher_order_knowledge', default=False, type=bool,
                        help="Specify whether the spies should use higher order knowledge")
    parser.add_argument('-rhok', '--resistance_higher_order_knowledge', default=False, type=bool,
                        help="Specify whether the resistance should use higher order knowledge")
    parser.add_argument('-iter', '--iterations', default=10, type=int,
                        choices=[1, 2, 5, 10, 15, 20],
                        help='Specify the number of iterations for each \
                        condition when running the simulation in batch mode')
    parser.add_argument('-debug', default=False, type=bool,
                        help="Set to true when debugging")
    return parser


parser = init_argparse()
options = parser.parse_args()
args = vars(options)


def get_identity_revealed(model):
    """Returns the round number at which the spies' identity was revealed"""
    return model.identity_revealed


def get_mission_results(model):
    """Returns an integer in bit-form indicating which rounds the spies won"""
    s = ""
    for i in model.rounds_won_spies:
        s = s + str(i)
    return int(s)


if options.run_mode == 'gui':
    server = ModelServer(N=options.number_of_agents, ps=options.party_size, debug=options.debug,
                         sphok=options.spies_higher_order_knowledge,
                         rhok=options.resistance_higher_order_knowledge)

    server.run_server()
elif options.run_mode == 'batch':
    fixed_params = {"S": 2,
                    "height": 5,
                    "width": 7,
                    "debug": options.debug}
    variable_params = {"sphok": [True, False],
                       "rhok": [True, False]}
    if options.number_of_agents == 5:
        variable_params['ps'] = ['2', 'def', '3']
        fixed_params['N'] = 5
    # Running the batchrunner for 6 agents skips the party size as a
    # variable parameter to reduce computation time.
    elif options.number_of_agents == 6:

        fixed_params['ps'] = 'def'
        fixed_params['N'] = 6

    batch_run = BatchRunner(ResistanceModel,
                            variable_params,
                            fixed_params,
                            iterations=options.iterations,
                            max_steps=50,
                            model_reporters={"rounds_won_spies": get_mission_results,
                                             "identity_revealed": get_identity_revealed})
    batch_run.run_all()
    run_data = batch_run.get_model_vars_dataframe()
    print(f"---------------Dependent variables----------------")
    print(f"levels rounds_won: {run_data['rounds_won_spies'].unique()}")
    print(f"levels identity_revealed: {run_data['identity_revealed'].unique()}")
    print(f"----------------independent variables-------------")
    print(f"levels N: {run_data['N'].unique()}")
    print(f"levels higher order knowledge spies: {run_data['sphok'].unique()}")
    print(f"levels higher order knowledge resistance: {run_data['rhok'].unique()}")
    print(f"levels ps: {run_data['ps'].unique()}")
    try:
        os.mkdir("results")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    with open('results' + os.path.sep + 'N_' + str(options.number_of_agents) +
              '_output.json', 'w') as outfile:
        run_data.to_json(outfile)
else:
    print("Please pick a valid option for the --run_mode flag")
# server = ModelServer()
#
# server.run_server()
