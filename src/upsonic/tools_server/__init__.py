



import uvicorn


def run_tools_server():
    uvicorn.run("upsonic.tools_server.server.api:app", host="0.0.0.0", port=8086, reload=True)


__all__ = ["app"]
