import ast
import operator
from langchain_core.tools import tool
from utils.logging_config import setup_logger, global_metrics

logger = setup_logger("calculator_tool")

# Supported operators for safe eval
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.BitXor: operator.xor,
    ast.USub: operator.neg
}

def safe_eval(expr: str):
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return OPERATORS[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(node)
    
    node = ast.parse(expr, mode='eval').body
    return _eval(node)

@tool
def calculate(expression: str) -> str:
    """Useful for when you need to answer questions about math. 
    Pass a valid mathematical expression as the input (e.g., '120 * 0.15').
    """
    logger.info(f"Tool called: calculate with expression: {expression}")
    global_metrics.increment_tool()
    try:
        result = safe_eval(expression)
        return str(result)
    except Exception as e:
        logger.error(f"Calculate tool failed: {e}")
        return f"Error evaluating expression: {str(e)}"
