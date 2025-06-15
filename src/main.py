from .models.clinica import Clinica
from .cli.cli import CLI

if __name__ == "__main__":
    clinica = Clinica({}, {}, [], {})

    cli = CLI(clinica)

    cli.run()
