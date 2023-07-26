import uvicorn


if __name__ == "__main__":
    uvicorn.run("blogapp:create_app", reload=True, factory=True)
