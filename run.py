import subprocess

def run():
    import engine
    engine.main()


if __name__=='__main__':
    try:
        run()
    except Exception as why:
        print(why)
        consent = input("Install Pygame?[Y/N]: ")
        if consent.lower() == 'y':
            subprocess.run(["pip", "install", "-r", "requirements.txt"])
            run()
