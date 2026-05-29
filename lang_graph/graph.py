from typing_extensions import TypedDict

class State(TypedDict):
    user_message : str
    ai_message : str
    is_coding : bool

def detect_query(state : State):
    user_message = state.get("user_message")
    
    #Open API call
    
    state.is_coding = True
    return state  

def solve_coding_question(state : State):
    user_message = state.get("user_message")
    
    #Open API call (solving question using gpt tool)
    state.ai_message = "Here is your coding question answer"
    return state
    
def solve_simple_question(state : State):
    user_message = state.get("user_message")
    
    #Open API call (solving question using gpt tool)
    state.ai_message = "Please ask some coding related questions"
    return state
    