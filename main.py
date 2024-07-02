import uvicorn

from create_fasapi_app import create_app

main_app = create_app(
    create_custom_static_urls=True,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
