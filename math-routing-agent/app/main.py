from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import MathQuestion, FeedbackRequest
from app.guardrails.ai_gateway import AIGateway
from app.knowledge_base.vector_db import MathKnowledgeBase
from app.mcp.web_search import MCPSearch
from app.agents.dspy_routing_agent import MathRoutingAgent
from app.agents.math_solver import MathSolverAgent
from app.agents.feedback_agent import HumanFeedbackAgent
from app.config import Config
import uvicorn

app = FastAPI(title="Math Routing Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize all components
ai_gateway = AIGateway()
knowledge_base = MathKnowledgeBase()
web_searcher = MCPSearch(api_key=Config.TAVILY_API_KEY)
routing_agent = MathRoutingAgent()
math_solver = MathSolverAgent()
feedback_agent = HumanFeedbackAgent()

@app.get("/")
async def root():
    return {"message": "Math Routing Agent API is running!", "status": "operational"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Math Agent",
        "components": {
            "knowledge_base": "active",
            "web_search": "active", 
            "routing": "active",
            "feedback_system": "active"
        }
    }

@app.post("/solve-math")
async def solve_math_problem(math_question: MathQuestion):
    """Main endpoint implementing Agentic RAG architecture"""
    try:
        # Step 1: AI Gateway - Input Guardrails
        input_validation = ai_gateway.process_input(math_question.question)
        if not input_validation["is_valid"]:
            raise HTTPException(status_code=400, detail=input_validation["error_message"])
        
        # Step 2: Knowledge Base Search (RAG)
        kb_results = knowledge_base.search_similar_questions(input_validation["sanitized_query"])
        
        # Step 3: Intelligent Routing
        routing_decision = routing_agent.route_question(
            input_validation["sanitized_query"], 
            kb_results
        )
        
        solution_data = None
        
        # Step 4: Route to appropriate solver
        if routing_decision["use_knowledge_base"] and kb_results:
            # Use Knowledge Base solution (RAG)
            best_match = kb_results[0]
            solution_data = math_solver.generate_solution_from_kb(
                input_validation["sanitized_query"],
                best_match["solution"]
            )
            solution_data["similar_question"] = best_match["question"]
            solution_data["similarity_score"] = best_match["similarity_score"]
            
        else:
            # Use Web Search with MCP
            web_results = web_searcher.search_math_solution(input_validation["sanitized_query"])
            
            if web_results["success"] and web_results["has_mathematical_content"]:
                solution_data = math_solver.generate_solution_from_web(
                    input_validation["sanitized_query"],
                    web_results
                )
            else:
                # Fallback to direct AI solution
                solution_data = math_solver.generate_solution_from_web(
                    input_validation["sanitized_query"],
                    {}
                )
        
        # Step 5: AI Gateway - Output Guardrails
        output_validation = ai_gateway.process_output(
            solution_data.get("final_answer", ""),
            solution_data.get("steps", [])
        )
        
        response_data = {
            "question": math_question.question,
            "solution": solution_data,
            "routing_decision": routing_decision,
            "formatted_solution": output_validation["formatted_solution"],
            "kb_matches_found": len(kb_results),
            "system_architecture": "Agentic-RAG with MCP"
        }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/provide-feedback")
async def provide_feedback(feedback_request: FeedbackRequest):
    """Human-in-the-loop feedback endpoint"""
    feedback_result = feedback_agent.process_feedback(
        feedback_request.question,
        feedback_request.original_solution,
        feedback_request.feedback
    )
    
    return feedback_result

@app.get("/feedback-stats")
async def get_feedback_stats():
    """Get feedback system statistics"""
    return feedback_agent.get_feedback_stats()

@app.get("/system-info")
async def system_info():
    """Get system architecture information"""
    return {
        "architecture": "Agentic-RAG with Human-in-the-Loop",
        "components": [
            "AI Gateway with Input/Output Guardrails",
            "Vector Database Knowledge Base", 
            "DSPy Intelligent Routing",
            "MCP Web Search Integration",
            "Human Feedback Learning System"
        ],
        "features": [
            "Privacy-protected input processing",
            "Educational content validation", 
            "Intelligent KB vs Web routing",
            "Continuous learning from feedback",
            "Step-by-step mathematical solutions"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)