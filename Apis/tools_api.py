import os
from dotenv import load_dotenv
from langchain.tools import StructuredTool
from pydantic import create_model, Field,BaseModel
import requests
import re
from typing import Optional



load_dotenv()




def create_api_tool(spec: dict) -> StructuredTool:
    type_map = {"string": str, "integer": int, "number": float, "boolean": bool}
    properties = spec["params"].get("properties", {})
    required = set(spec["params"].get("required", []))

    fields = {
        name: (
            type_map[prop["type"].lower()],
            Field(... if name in required else None, description=prop.get("description", ""))
        )
        for name, prop in properties.items()
    }

    # If no fields, define a dummy no-param model
    if not fields:
        class NoParams(BaseModel):
            pass
        ParamsModel = NoParams
    else:
        ParamsModel = create_model(f"{spec['name'].title()}Params", **fields)

    path_param_names = set(re.findall(r"{(\w+)}", spec["endpoint"]))

    def api_caller(params: Optional[ParamsModel] = None):
        all_params = params.model_dump() if params else {}
        method = spec["method"].upper()
        formatted_url = spec["endpoint"].format(**all_params)
        other_params = {k: v for k, v in all_params.items() if k not in path_param_names}

        if method == "GET":
            response = requests.get(formatted_url, params=other_params)
        elif method == "POST":
            response = requests.post(formatted_url, json=other_params)
        elif method == "PUT":
            response = requests.put(formatted_url, json=other_params)
        elif method == "DELETE":
            response = requests.delete(formatted_url, json=other_params)
        else:
            raise ValueError(f"Unsupported method: {method}")

        return response.text

    return StructuredTool(
        name=spec["name"],
        description=spec["description"],
        func=api_caller,
        args_schema=ParamsModel
    )




