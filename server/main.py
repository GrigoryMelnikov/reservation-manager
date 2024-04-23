import uvicorn
from fastapi import FastAPI

app = FastAPI()
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

@app.get('/')
async def root():
    return {"Hello", "World"}

def __init__():
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port='8000',
        debug=False,
        reload=True,
        reload_includes=["*"]
    )