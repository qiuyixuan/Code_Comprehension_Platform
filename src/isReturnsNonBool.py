from xmlrpc.client import Boolean
import astroid
from astroid import nodes
from typing import TYPE_CHECKING, Optional

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


"""
Checks if an is method returns a non boolean
Put this file in <python directory>\Lib\site-packages\pylint\checkers
"""

def register(linter: "PyLinter") -> None:
    """This required method auto registers the checker during initialization.
    :param linter: The linter to register the checker to.
    """
    linter.register_checker(isReturnsNonBool(linter))

class isReturnsNonBool(BaseChecker):
    __implements__ = IAstroidChecker

    name = "is-returns-non-bool"
    msgs = {
        "C1441": (
            "Is method returns a non boolean.",
            "is-returns-non-bool",
            "An is method should return a boolean.",
        ),
    }
    options = (
        (
            "is-returns-non-bool",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Allow is methods to return non booleans",
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
        if(node.value!=None and type(node.value.value)!=Boolean and self.funcNames[-1][:2]=="is"):
            self.add_message("is-returns-non-bool",node = node)

        self._function_stack[-1].append(node)
    
