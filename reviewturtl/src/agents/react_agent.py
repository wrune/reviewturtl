from reviewturtl.src.programmes.programmes import (
    TypedChainOfThoughtProgramme as DspyProgramme,
)
from reviewturtl.src.signatures.signatures import (
    ReactSignature,
    FindArgumentsForAgent,
    FinalResponseConstructor,
)
from reviewturtl.src.agents.base_agent import Agent
from reviewturtl.src.agents.utils import agent_dict
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

log = logging.getLogger(__name__)


class ReactAgent(Agent):
    def __init__(self):
        self.class_name = __class__.__name__
        self.input_variables = ["conversation_history", "query", "available_agents"]
        self.output_variables = ["response"]
        self.desc = "A react agent that processes a query and conversation history to provide a response."
        super().__init__(DspyProgramme(signature=ReactSignature))
        self.argument_finder = DspyProgramme(signature=FindArgumentsForAgent)
        self.final_response_constructor = DspyProgramme(
            signature=FinalResponseConstructor
        )

    def forward(self, conversation_history, query, context, model=None):
        """
        This function runs the React Agent programme to get the response.
        Args:
            conversation_history (str): The conversation history.
            query (str): The query to be processed.
            context (str): The context to be used.
            model (str): The model to be used.
        Returns:
            response (str): The response to the query.
        """
        available_agents_with_desc = {
            agent["class_name"]: agent["description"] for agent in agent_dict.values()
        }
        log.info(f"Provided Agents: {available_agents_with_desc}")
        self.prediction_object = self.programme.forward(
            conversation_history=conversation_history,
            query=query,
            available_agents=available_agents_with_desc,
            model=model,
        )
        agents_to_use = self.get_agents_to_use()
        log.info(f"Agents to use: {agents_to_use}")
        # let's maintain {"agent_being_used":args_for_agents}
        agent_caller = {}
        for agent in agents_to_use:
            agent_being_used = agent
            # let's make a dictionary with agent_being_used_with_desc = {agents_dict[agent_being_used]: agent_being_used}
            agent_being_used_with_desc = {
                agent_dict[agent_being_used]["class_name"]: agent_dict[
                    agent_being_used
                ]["description"]
            }
            log.info(f"Agent Being Used With Desc: {agent_being_used_with_desc}")
            # let's get the arguments to find for the agent
            args_to_find = agent_dict[agent_being_used]["input_variables"]
            log.info(f"Args to find: {args_to_find}")
            # let's get the arguments for the agent
            args_for_agents = self.args_for_agents(
                context, agent_being_used_with_desc, args_to_find, model=model
            )
            # let's add the arguments for the agent to the agent_caller dictionary
            agent_caller[agent_being_used] = args_for_agents
        # now let's initialize and call the agents properly
        log.info(f"Agent Caller: {agent_caller}")
        all_prediction_objects = {}
        for agent_being_used in agents_to_use:
            args_for_agent = agent_caller[agent_being_used]
            agent_object = agent_dict[agent_being_used]["class_object"]
            log.info(f"Args for agent: {args_for_agent}")
            try:
                prediction_object_from_agent = agent_object(**args_for_agent)
                all_prediction_objects[agent_being_used] = prediction_object_from_agent
            except Exception as e:
                log.error(
                    f"Error calling agent: {agent_being_used} with args: {args_for_agent} with error: {e}",
                    exc_info=True,
                )
                continue
        # Final Response Constructor using the preidction objects from several agents
        final_response = self.final_response_constructor.forward(
            conversation_history=conversation_history,
            query=query,
            available_agents=available_agents_with_desc,
            all_prediction_objects=all_prediction_objects,
        ).final_response
        return final_response

    def run_agent_finder(self, conversation_history, query, available_agents_with_desc):
        """
        This function runs the agent finder programme to get the agents to use.
        """
        return self.programme.forward(
            conversation_history=conversation_history,
            query=query,
            available_agents=available_agents_with_desc,
        ).agents_to_use

    def get_agents_to_use(self):
        return self.prediction_object.agents_to_use

    def args_for_agents(
        self, context, agents_to_use_with_desc, arguments_to_find, model=None
    ):
        """
        Run the Argument Finder programme to get the arguments for the agents.
        """
        args_for_agents = self.argument_finder.forward(
            context=context,
            agent_being_used_with_desc=agents_to_use_with_desc,
            arguments_to_find=arguments_to_find,
            model=model,
        )
        return args_for_agents.args_with_values

    def __call__(self, conversation_history, query, context, model=None):
        return self.forward(conversation_history, query, context, model=model)


__all__ = ["ReactAgent"]
