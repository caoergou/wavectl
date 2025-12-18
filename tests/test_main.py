from typer.testing import CliRunner
from wavectl.main import app

runner = CliRunner()

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "WaveCtl: Interactive WaveTerm Configuration Manager." in result.stdout
