def node_to_string(node):
    ast_type = node["ast_type"]
    if ast_type == "Module":
        return node_to_string(node["body"])
    elif ast_type == "FunctionDef":
        return f"def {node['name']}({node_to_string(node['args'])}):"
    elif ast_type == "arguments":
        return ", ".join([node_to_string(arg) for arg in node["args"]])
    elif ast_type == "arg":
        return node["arg"]
    elif ast_type == "Expr":
        return node_to_string(node["value"])
    elif ast_type == "Call":
        return f"{node_to_string(node['func'])}({node_to_string(node['args'])})"
    elif ast_type == "Name":
        return node["id"]
    elif ast_type == "Constant":
        return str(node["value"])
    elif ast_type == "BinOp":
        return f"{node_to_string(node['left'])} {node['op']} {node_to_string(node['right'])}"
    elif ast_type == "Return":
        return f"return {node_to_string(node['value'])}"
    elif ast_type == "Assign":
        return f"{node_to_string(node['targets'])} = {node_to_string(node['value'])}"
    elif ast_type == "List":
        return f"[{node_to_string(node['elts'])}]"
    elif ast_type == "Subscript":
        return f"{node_to_string(node['value'])}[{node_to_string(node['slice'])}]"
    elif ast_type == "Index":
        return node_to_string(node["value"])
    elif ast_type == "Slice":
        return f"{node_to_string(node['lower'])}:{node_to_string(node['upper'])}"
    elif ast_type == "Attribute":
        return f"{node_to_string(node['value'])}.{node['attr']}"
    elif ast_type == "If":
        return f"if {node_to_string(node['test'])}:"
    elif ast_type == "Compare":
        return f"{node_to_string(node['left'])} {node_to_string(node['ops'])} {node_to_string(node['comparators'])}"
    elif ast_type == "Eq":
        return "=="
    elif ast_type == "Gt":
        return ">"
    elif ast_type == "Lt":
        return "<"
    elif ast_type == "GtE":
        return ">="

def convert_ast_to_string(ast, config):
    ## Handle the config and ast tabs
    return node_to_string(ast["ast"])