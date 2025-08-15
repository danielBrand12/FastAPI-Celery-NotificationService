from os import getenv


def initialize_fastapi_server_debugger_if_needed():
    print("Checking if FastAPI server debugger should be initialized...")
    if getenv("DEBUGGER") == "True":
        print("Debugger is enabled, initializing FastAPI server debugger...")
        # import multiprocessing

        # print(multiprocessing.current_process().pid > 1)

        # if multiprocessing.current_process().pid > 1:
        import debugpy

        debugpy.listen(("0.0.0.0", 10004))
        print(
            "⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳",
            flush=True,
        )
        debugpy.wait_for_client()
        print("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)