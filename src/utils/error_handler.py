from typing import Any, Dict


class ErrorHandler:
    @staticmethod
    def add_error(state: Dict[str, Any], message: str) -> Dict[str, Any]:
        errors = state.get("errors", [])
        errors.append(message)
        return {**state, "errors": errors}
