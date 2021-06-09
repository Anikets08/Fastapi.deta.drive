from deta import Deta
from fastapi import FastAPI, UploadFile, File
from localFile import key
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI()
deta = Deta(key)
drive = deta.Drive("images")

@app.get("/", response_class=HTMLResponse)
def render():
    return """
    <form action="/upload" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit">
    </form>
    """

@app.post("/upload")
def upload_img(file: UploadFile = File(...)):
    name = file.filename
    f = file.file
    res = drive.put(name, f)
    return res

@app.get("/download/{name}")
def download_img(name: str):
    res = drive.get(name)
    return StreamingResponse(res.iter_chunks(1080), media_type="image/png")



