import typer

def main(name:str,
         age:int = typer.Option()):
    typer.echo("Hello World")


if __name__ == "__main__":
    # typer.run(main)
    print("hello")