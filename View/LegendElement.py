from mesa.visualization.modules import TextElement


class LegendElement(TextElement):
    def render(self, model):
        jqueryMove = """
        <script>
        jQuery("#legend").appendTo(jQuery("#sidebar"));
        </script> """
        legend = """ 
            <div id='legend' class="border">
            <h3>
                Legend
            </h3>
            <p>
            This is a simulation of the resistance game. Agents are initialized at the bottom of the grid represented
            by the circles. However, not all agents are who they say there are! Some agents are actually spies trying
            to undermine the efforts of the resistance.
            </p>

            An true member of the resistance: <br>
            <span>
            <div class="agent" style="background-color: blue">
            </div>
            </span>
            <br> A spy: <br>
            <div class="agent" style="background-color: red">
            </div>
            <p>
            There are several settings that influence the working of the game. Changing these settings can be done by
            running 'python3 RunSimulation.py' with the appropriate flags. Run 'python3 RunSimulation.py -h' for more 
            information
            <h4>Current settings</h4>
            Number of agents: """ + str(model.num_agents) + """ <br>
            Size of the mission parties: """ + str(model.ps) + """  <br>
            Use of higher order knowledge of the resistance: """ + str(model.resistance_reasons) + """ <br>
            Use of higher order knowledge of the spies: """ + str(model.spy_reasons) + """ <br>
            </div>
            <style>
            .agent {
                height: 30px;
                width: 30px;
                border-radius: 50%;
                display: inline-block;
                border: 1px solid;
            }
            #elements #legend {
                display: none;
            }
            </style>
                """
        return legend + jqueryMove