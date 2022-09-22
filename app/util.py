from . import db,models,crud,app


from flask import request, url_for



def is_valid_password(username,password):
    if crud.get_password(username)==password:
        return True
    else:
        return False

@app.context_processor
def add_jinja_utils() -> dict:
    def is_endpoint(func: str) -> bool:
        path: str = request.path
        endpoint = url_for(func)
        return path == endpoint

    

    return dict(
        is_endpoint=is_endpoint,
        
    )