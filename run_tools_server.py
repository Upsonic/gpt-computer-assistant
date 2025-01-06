import uvicorn


def main():
    uvicorn.run(
        "upsonicai.server.tools.server.api:app", host="0.0.0.0", port=8086, reload=True
    )


if __name__ == "__main__":
    main()
