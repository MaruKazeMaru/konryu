import os
import subprocess

def test_cli():
    subprocess.run(
        [
            "konryu",
            os.path.join("data", "plan.txt")
        ],
        cwd=os.path.dirname(__file__)
    )


if __name__ == "__main__":
    test_cli()
