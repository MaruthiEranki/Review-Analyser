from fastapi import FastAPI

app = FastAPI(title="Review Analyzer")


@app.get("/")
def root():
    return {"message": "Review Analyzer API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
