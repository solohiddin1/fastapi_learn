from fastapi.responses import JSONResponse

def success_response(data: dict=None, status_code: int = 200):
    return JSONResponse(
        content={"success": True, "data": data}, 
        status_code=status_code)