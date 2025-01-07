import uvicorn


def main():
    uvicorn.run("upsonic.server.api:app", host="0.0.0.0", port=8087, reload=True)


if __name__ == "__main__":
    main()
