from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import qrcode
from io import BytesIO, StringIO
from qrcode.image.pil import PilImage
from qrcode.image.svg import SvgPathImage
from qrcode.image.pure import PyPNGImage
from qrcode.image.styledpil import StyledPilImage
import zipfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QRCodeRequest(BaseModel):
    data: str = Field(..., min_length=1, max_length=4296)
    error_correction: str = Field("M", pattern="^[LMQH]$")
    version: int = Field(0, ge=0, le=40)
    box_size: int = Field(10, ge=1)
    border: int = Field(4, ge=0)
    fill_color: str = Field("#000000", pattern="^#[0-9A-Fa-f]{6}$")
    back_color: str = Field("#FFFFFF", pattern="^#[0-9A-Fa-f]{6}$")
    format: str = Field("PNG", pattern="^(PNG|SVG|PURE_PNG)$")
    style: str = Field("standard", pattern="^(standard|rounded)$")

class BatchQRCodeRequest(BaseModel):
    items: list[QRCodeRequest]

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/generate-qr")
async def generate_qr(request: QRCodeRequest):
    try:
        error_correction_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }
        error_correction = error_correction_map.get(request.error_correction, qrcode.constants.ERROR_CORRECT_M)

        qr = qrcode.QRCode(
            version=request.version if request.version > 0 else None,
            error_correction=error_correction,
            box_size=request.box_size,
            border=request.border
        )
        qr.add_data(request.data)
        qr.make(fit=True)

        if request.format.upper() == "SVG":
            img = qr.make_image(fill_color=request.fill_color, back_color=request.back_color, image_factory=SvgPathImage)
            img_byte_arr = StringIO()
            img.save(img_byte_arr)
            img_byte_arr.seek(0)
            return StreamingResponse(img_byte_arr, media_type="image/svg+xml")
        elif request.format.upper() == "PURE_PNG":
            img = qr.make_image(fill_color=request.fill_color, back_color=request.back_color, image_factory=PyPNGImage)
            img_byte_arr = BytesIO()
            img.save(img_byte_arr)
            img_byte_arr.seek(0)
            return StreamingResponse(img_byte_arr, media_type="image/png")
        else:
            image_factory = StyledPilImage if request.style == "rounded" else PilImage
            img = qr.make_image(fill_color=request.fill_color, back_color=request.back_color, image_factory=image_factory)
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return StreamingResponse(img_byte_arr, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-qr-ascii")
async def generate_qr_ascii(request: QRCodeRequest):
    try:
        error_correction_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }
        error_correction = error_correction_map.get(request.error_correction, qrcode.constants.ERROR_CORRECT_M)

        qr = qrcode.QRCode(
            version=request.version if request.version > 0 else None,
            error_correction=error_correction,
            box_size=request.box_size,
            border=request.border
        )
        qr.add_data(request.data)
        qr.make(fit=True)

        output = StringIO()
        qr.print_ascii(out=output)
        output.seek(0)
        return {"ascii": output.getvalue()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-qr-matrix")
async def generate_qr_matrix(request: QRCodeRequest):
    try:
        error_correction_map = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }
        error_correction = error_correction_map.get(request.error_correction, qrcode.constants.ERROR_CORRECT_M)

        qr = qrcode.QRCode(
            version=request.version if request.version > 0 else None,
            error_correction=error_correction,
            box_size=request.box_size,
            border=request.border
        )
        qr.add_data(request.data)
        qr.make(fit=True)

        matrix = qr.get_matrix()
        return {"matrix": matrix}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-qr-batch")
async def generate_qr_batch(request: BatchQRCodeRequest):
    try:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, item in enumerate(request.items):
                error_correction_map = {
                    "L": qrcode.constants.ERROR_CORRECT_L,
                    "M": qrcode.constants.ERROR_CORRECT_M,
                    "Q": qrcode.constants.ERROR_CORRECT_Q,
                    "H": qrcode.constants.ERROR_CORRECT_H
                }
                error_correction = error_correction_map.get(item.error_correction, qrcode.constants.ERROR_CORRECT_M)

                qr = qrcode.QRCode(
                    version=item.version if item.version > 0 else None,
                    error_correction=error_correction,
                    box_size=item.box_size,
                    border=item.border
                )
                qr.add_data(item.data)
                qr.make(fit=True)

                img_byte_arr = BytesIO() if item.format.upper() != "SVG" else StringIO()
                if item.format.upper() == "SVG":
                    img = qr.make_image(fill_color=item.fill_color, back_color=item.back_color, image_factory=SvgPathImage)
                    img.save(img_byte_arr)
                    ext = "svg"
                elif item.format.upper() == "PURE_PNG":
                    img = qr.make_image(fill_color=item.fill_color, back_color=item.back_color, image_factory=PyPNGImage)
                    img.save(img_byte_arr)
                    ext = "png"
                else:
                    image_factory = StyledPilImage if item.style == "rounded" else PilImage
                    img = qr.make_image(fill_color=item.fill_color, back_color=item.back_color, image_factory=image_factory)
                    img.save(img_byte_arr, format='PNG')
                    ext = "png"
                img_byte_arr.seek(0)
                zip_file.writestr(f"qrcode_{i}.{ext}", img_byte_arr.getvalue())

        zip_buffer.seek(0)
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=qrcodes.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))