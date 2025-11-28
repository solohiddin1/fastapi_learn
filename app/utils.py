from fastapi.responses import JSONResponse

def success_response(data: dict=None, status_code: int = 200):
    return JSONResponse(
        content={"success": True, "data": data}, 
        status_code=status_code)

def error_response(data: str=None, status_code: int=400):
    return JSONResponse(
        content={"success": False, "data": data}, 
        status_code=status_code)
