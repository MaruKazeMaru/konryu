import os
import subprocess

def test_cli():
    ret = subprocess.run(
        [
            "konryu",
            os.path.join("data", "plan.txt")
        ],
        cwd=os.path.dirname(__file__),
        capture_output=True,
        text=True
    )
    assert ret.returncode == 0
    assert ret.stdout == ""

    ret = subprocess.run(
        [
            "konryu",
            os.path.join("data", "plan.txt"),
            "--log"
        ],
        cwd=os.path.dirname(__file__),
        capture_output=True,
        text=True
    )
    assert ret.returncode == 0
    assert ret.stdout != ""


if __name__ == "__main__":
    test_cli()
