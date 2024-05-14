
def run(app,port):
    import sys
    sys.PORT_NUMBER = port
    is_live = "ubuntu" in sys.argv[0]
    if is_live:
        import uvicorn
        uvicorn.run(app+":app", host="0.0.0.0", port=port, ssl_keyfile="MAIN/privkey.pem", ssl_certfile="MAIN/fullchain.pem")
    else:
        import uvicorn
        uvicorn.run(app+":app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    pass
    # run("vellore",50088)
    # run("virar",50087)
    run("talentov",5000)

