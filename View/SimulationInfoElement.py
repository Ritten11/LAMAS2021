
from mesa.visualization.modules import TextElement


class SimulationInfoElement(TextElement):
    def render(self, model):
        jqueryMove = """
                <script>
                jQuery("#legend").appendTo(jQuery("#sidebar"));
                </script> """
        infoText = """
        <div>
        <h2>Simulation info</h2>
        <p>Current mission leader: """ + str(model.mission_leader) + """ </p>
        <p>Current mission team: """ + str(model.mission_team) + """ </p>
        <p>Set of possible worlds: """ + str(model.kripke_model.ks.get_power_set_of_worlds()[-1]) + """</p>
        <p> """ + model.ui_message + """</p>
        </div >
        """
        return infoText + jqueryMove