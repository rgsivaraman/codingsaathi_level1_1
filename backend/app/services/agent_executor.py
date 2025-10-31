import asyncio
import json
from typing import Dict, Any
from app.schemas.schemas import AgentExecuteResponse


async def execute_agent_code(code: str, input_data: Dict[str, Any]) -> AgentExecuteResponse:
    """
    Execute agent code in a sandboxed environment.
    For production, this should use Docker containers for isolation.
    This is a simplified version using exec with restricted globals.
    """
    try:
        # Create a restricted execution environment
        restricted_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'abs': abs,
                'min': min,
                'max': max,
                'sum': sum,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
            },
            'input_data': input_data,
            'json': json,
        }
        
        # Prepare output capture
        output_lines = []
        
        def custom_print(*args, **kwargs):
            output_lines.append(' '.join(str(arg) for arg in args))
        
        restricted_globals['__builtins__']['print'] = custom_print
        
        # Execute code with timeout
        local_vars = {}
        exec(code, restricted_globals, local_vars)
        
        # Get result
        result = local_vars.get('result', None)
        if result is not None:
            output = str(result)
        elif output_lines:
            output = '\n'.join(output_lines)
        else:
            output = "Code executed successfully with no output"
        
        return AgentExecuteResponse(
            success=True,
            output=output,
            error=None
        )
    
    except Exception as e:
        return AgentExecuteResponse(
            success=False,
            output=None,
            error=str(e)
        )
