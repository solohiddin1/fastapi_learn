from fastapi.responses import JSONResponse
from app.utils.enum import ResultCodes, ResultMessages
from fastapi import status

def success_response(data: dict=None, status_code: int = 200):
    return JSONResponse(
        content={"success": True, "data": data}, 
        status_code=status_code)

def error_response(result: ResultCodes, message: dict=None):
    return JSONResponse(
        content={"success": False, "error": {
            "code": result.value,
            "message": ResultMessages[result.name],
            "data": message
        }},
        status_code=status.HTTP_200_OK)
