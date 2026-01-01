import json
import sys
import os

sys.path.append(os.getcwd())

import main


async def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"})
        }

    try:
        payload = request.json or {}

        tool_name = payload.get("tool")
        tool_input = payload.get("input", {})

        if not tool_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing tool name"})
            }

        # Call FastMCP tool
        result = await main.mcp.call_tool(tool_name, tool_input)

        # 🔑 UNWRAP MCP CONTENT
        if hasattr(result, "text"):
            output = result.text
        else:
            # Fallback for future content types
            output = str(result)

        return {
            "statusCode": 200,
            "body": json.dumps({"result": output})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
