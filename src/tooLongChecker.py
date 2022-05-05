import astroid
from astroid import nodes
from typing import TYPE_CHECKING, Optional

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


"""
Checks if a get method returns nothing
Put this file in <python directory>\Lib\site-packages\pylint\checkers
"""

def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.
    :param linter: The linter to register the checker to.
    """
    linter.register_checker(MethodTooLong(linter))

class MethodTooLong(BaseChecker):
    __implements__ = IAstroidChecker

    name = "method-too-long"
    msgs = {
        "C1325": (
            "Method name too long.",
            "method-too-long",
            "Consider shortening this method name.",
        ),
    }
    options = (
        (
            "method-too-long",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Allow longer method names",
            },
        ),
    )
    def __init__(self, linter: Optional["PyLinter"] = None) -> None:
        super().__init__(linter)
        self._function_stack = []
        self.funcNames = []

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        self._function_stack.append([])
        self.funcNames.append(node.name)
        if(len(self.funcNames[-1])>12):
            self.add_message("method-too-long",node = node)


    def leave_functiondef(self, node: nodes.FunctionDef) -> None:
        self._function_stack.pop()
        self.funcNames.pop()
    
    def visit_return(self, node: nodes.Return) -> None:
        self._function_stack[-1].append(node)
    
