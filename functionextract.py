import ast

class FunctionExtractor(ast.NodeVisitor):
    def __init__(self, function_name):
        self.function_name = function_name
        self.function_code = None

    def visit_FunctionDef(self, node):
        if node.name == self.function_name:
            self.function_code = ast.get_source_segment(self.source_code, node)
        self.generic_visit(node)

def extract_function_code(file_path, function_name):
    with open(file_path, 'r') as file:
        source_code = file.read()
    
    tree = ast.parse(source_code)
    extractor = FunctionExtractor(function_name)
    extractor.source_code = source_code
    extractor.visit(tree)
    
    return extractor.function_code

