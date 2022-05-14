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
    linter.register_checker(GetReturns(linter))

class GetReturns(BaseChecker):
    __implements__ = IAstroidChecker

    name = "get-returns"
    msgs = {
        "C4141": (
            "Get method returns nothing.",
            "get-no-return",
            "A get method should return something.",
        ),
    }
    options = (
        (
            "ignore-ints",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Allow get methods to return nothing",
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

    def leave_functiondef(self, node: nodes.FunctionDef) -> None:
        self._function_stack.pop()
        self.funcNames.pop()
    
    def visit_return(self, node: nodes.Return) -> None:
        if(node.value==None and self.funcNames[-1][:3]=="get"):
            self.add_message("get-no-return",node = node)

        self._function_stack[-1].append(node)
    
