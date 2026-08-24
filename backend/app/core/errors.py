from typing import Any


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        fields: dict[str, list[str]] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.fields = fields
        super().__init__(message)


def error_body(code: str, message: str, fields: dict[str, list[str]] | None = None) -> dict[str, Any]:
    err: dict[str, Any] = {"code": code, "message": message}
    if fields:
        err["fields"] = fields
    return {"success": False, "error": err}


def success_body(data: Any, pagination: dict[str, Any] | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {"success": True, "data": data}
    if pagination is not None:
        body["pagination"] = pagination
    return body
