from fastapi import FastAPI

app = FastAPI(
    title="Meta Earth VN Backend",
    description="Backend API cho dự án Meta Earth VN",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Backend Meta Earth VN đang chạy"}