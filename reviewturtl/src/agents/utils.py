from reviewturtl.src.agents.summarizer_agent import SummarizerAgent
from reviewturtl.src.agents.code_search_agent import CodeSearchAgent

agents = [SummarizerAgent, CodeSearchAgent]

_initialized = False  # Module-level flag to ensure initialization runs only once


def init_agentic_mappers():
    global _initialized
    if not _initialized:
        agent_dict = {}
        for agent in agents:
            agent_init = agent()
            agent_dict[agent_init.class_name] = {
                "class_name": agent_init.class_name,
                "description": agent_init.desc,
                "input_variables": agent_init.input_variables,
                "class_object": agent_init,
            }
        _initialized = True
    return agent_dict


agent_dict = init_agentic_mappers()
