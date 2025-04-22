import ast
import resource


class UnsafeCodeError(Exception):
    pass


def validate_ast(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise UnsafeCodeError("Import statements are not allowed.")
        if isinstance(node, ast.With):
            raise UnsafeCodeError("With statements are not allowed.")
        if isinstance(node, ast.Call):
            func = getattr(node.func, 'id', '') or getattr(node.func, 'attr', '')
            if func in {'exec', 'eval', 'open', 'compile', '__import__'}:
                raise UnsafeCodeError(f"Use of '{func}' is not allowed.")
    return True


def limit_resources():
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    resource.setrlimit(resource.RLIMIT_AS, (64 * 1024 * 1024, 64 * 1024 * 1024))
