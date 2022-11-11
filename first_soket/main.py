from fastapi import FastAPI, WebSocket, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger 
from log  import LOG

app = FastAPI()

templates = Jinja2Templates(directory="../templates")

@app.get("/client")
async def client(request : Request):
    return templates.TemplateResponse("client.html",{"request" : request})

@app.websocket("/ws")
async def websoket_endpoint(websoket : WebSocket):
    print(f"client connected : {websoket.client}")
    await websoket.accept()
    await websoket.send_text(f"Welcome client : {websoket.client}")
    
    while True:
        data = await websoket.receive_text()
        print(f"message received : {data} from : {websoket.client}")
        LOG.error(data)
        await websoket.send_text(f"Message text was : {data}") 
        
def run():
    import uvicorn
    uvicorn.run(app)
    
if __name__ == "__main__":
    run()