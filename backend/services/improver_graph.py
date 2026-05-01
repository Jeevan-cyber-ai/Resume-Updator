import os
from typing import TypedDict, Any, Dict, List
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from prompts.improve import IMPROVE_OBJECTIVE_PROMPT, IMPROVE_PROJECTS_PROMPT, IMPROVE_SKILLS_PROMPT, IMPROVE_TITLE_PROMPT

class ImproverState(TypedDict):
    section: str
    resume_data: Dict[str, Any]
    job_title: str
    user_input: str
    feedback_history: List[Dict[str, str]]
    generated_output: str

def format_feedback(feedback_history: List[Dict[str, str]]) -> str:
    if not feedback_history:
        return "No previous feedback."
    return "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in feedback_history])

def improve_title_node(state: ImproverState) -> ImproverState:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.7, google_api_key=api_key)
    
    prompt = PromptTemplate.from_template(IMPROVE_TITLE_PROMPT)
    chain = prompt | llm | StrOutputParser()
    
    experience_str = str(state["resume_data"].get("experience", []))
    
    output = chain.invoke({
        "job_title": state["job_title"],
        "experience": experience_str,
        "feedback_history": format_feedback(state.get("feedback_history", []))
    })
    
    state["generated_output"] = output.strip()
    return state

def improve_objective_node(state: ImproverState) -> ImproverState:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.7, google_api_key=api_key)
    
    prompt = PromptTemplate.from_template(IMPROVE_OBJECTIVE_PROMPT)
    chain = prompt | llm | StrOutputParser()
    
    experience_str = str(state["resume_data"].get("experience", []))
    
    output = chain.invoke({
        "job_title": state["job_title"],
        "experience": experience_str,
        "user_input": state["user_input"],
        "feedback_history": format_feedback(state.get("feedback_history", []))
    })
    
    state["generated_output"] = output.strip()
    return state

def improve_projects_node(state: ImproverState) -> ImproverState:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.7, google_api_key=api_key)
    
    prompt = PromptTemplate.from_template(IMPROVE_PROJECTS_PROMPT)
    chain = prompt | llm | StrOutputParser()
    
    output = chain.invoke({
        "job_title": state["job_title"],
        "user_input": state["user_input"],
        "feedback_history": format_feedback(state.get("feedback_history", []))
    })
    
    state["generated_output"] = output.strip()
    return state

def improve_skills_node(state: ImproverState) -> ImproverState:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.5, google_api_key=api_key)
    
    prompt = PromptTemplate.from_template(IMPROVE_SKILLS_PROMPT)
    chain = prompt | llm | StrOutputParser()
    
    current_skills_str = ", ".join(state["resume_data"].get("skills", []))
    
    output = chain.invoke({
        "job_title": state["job_title"],
        "current_skills": current_skills_str,
        "feedback_history": format_feedback(state.get("feedback_history", []))
    })
    
    state["generated_output"] = output.strip()
    return state

def route_section(state: ImproverState) -> str:
    section = state["section"].lower()
    if section == "title":
        return "improve_title"
    elif section in ["objective", "summary"]:
        return "improve_objective"
    elif section == "projects":
        return "improve_projects"
    elif section == "skills":
        return "improve_skills"
    else:
        # Default or fallback
        return END

# Build the Graph
workflow = StateGraph(ImproverState)

workflow.add_node("improve_title", improve_title_node)
workflow.add_node("improve_objective", improve_objective_node)
workflow.add_node("improve_projects", improve_projects_node)
workflow.add_node("improve_skills", improve_skills_node)

# We use conditional edges from the START node based on the 'section' in the state
workflow.set_conditional_entry_point(
    route_section,
    {
        "improve_title": "improve_title",
        "improve_objective": "improve_objective",
        "improve_projects": "improve_projects",
        "improve_skills": "improve_skills",
        END: END
    }
)

workflow.add_edge("improve_title", END)
workflow.add_edge("improve_objective", END)
workflow.add_edge("improve_projects", END)
workflow.add_edge("improve_skills", END)

# Compile the graph
improver_app = workflow.compile()

def run_improver_graph(state: dict) -> dict:
    """Entry point to run the compiled LangGraph app."""
    return improver_app.invoke(state)
