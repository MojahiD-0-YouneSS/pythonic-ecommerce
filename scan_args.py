import ast
import os

def scan_project(root_dir):
    # Pass 1: Find all functions that take strictly 0 arguments
    zero_arg_funcs = {} # name -> filepath, line

    for dirpath, _, filenames in os.walk(root_dir):
        if '.venv' in dirpath or 'migrations' in dirpath or '__pycache__' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=filepath)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            # Check if it takes 0 args and no kwargs/args
                            args = node.args
                            if not args.args and not args.vararg and not args.kwarg and not args.kwonlyargs:
                                zero_arg_funcs[node.name] = (filepath, node.lineno)
                except Exception as e:
                    pass

    # Pass 2: Find all calls to these functions with arguments
    mismatches = []
    
    for dirpath, _, filenames in os.walk(root_dir):
        if '.venv' in dirpath or 'migrations' in dirpath or '__pycache__' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=filepath)
                    for node in ast.walk(tree):
                        # 1. Direct Calls
                        if isinstance(node, ast.Call):
                            if isinstance(node.func, ast.Name):
                                func_name = node.func.id
                                if func_name in zero_arg_funcs:
                                    if node.args or node.keywords:
                                        mismatches.append((func_name, filepath, node.lineno, "Called with args", zero_arg_funcs[func_name]))
                        
                        # 2. Used in a pipeline (Tuple with a string as first element)
                        if isinstance(node, ast.Dict) or isinstance(node, ast.Set):
                            # In Python, {'string', func} parses as ast.Set if there are no colons
                            pass # We can just look for ast.Name usage inside AST Sets
                            
                    # Let's just find any reference to zero_arg_funcs inside a Set (which is how {'order', MyFunc} is parsed)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Set):
                            has_str = any(isinstance(elt, ast.Constant) and isinstance(elt.value, str) for elt in node.elts)
                            has_name = [elt for elt in node.elts if isinstance(elt, ast.Name)]
                            if has_str and has_name:
                                for name_node in has_name:
                                    func_name = name_node.id
                                    if func_name in zero_arg_funcs:
                                        mismatches.append((func_name, filepath, name_node.lineno, "Used in pipeline (will receive **dvars)", zero_arg_funcs[func_name]))

                except Exception as e:
                    pass

    for func_name, use_file, use_line, reason, (def_file, def_line) in mismatches:
        print(f"Warning: {func_name}")
        print(f"  Defined with 0 args at: {def_file}:{def_line}")
        print(f"  {reason} at: {use_file}:{use_line}")
        print("-" * 60)

if __name__ == "__main__":
    scan_project(r"C:\Users\mojahid\Desktop\youness\pythonic-ecommerce")
