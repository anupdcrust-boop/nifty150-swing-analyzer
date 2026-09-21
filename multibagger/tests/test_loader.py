"""Round-trips a dossier through JSON (dataclass -> dict -> load_dossier) and
checks every ReturnBridgeAssumptions field survives. Exists because the
loader silently dropped new fields once before (margin_delta_evidenced) --
a dataclass default masked it until a real run's numbers looked wrong."""

from dataclasses import asdict, is_dataclass
from enum import Enum

from multibagger.loader import load_dossier
from .fixtures import make_dossier


def _to_plain_json_dict(dossier):
    def convert(o):
        if isinstance(o, Enum):
            return o.name
        if is_dataclass(o):
            return {k: convert(v) for k, v in asdict(o).items()}
        if isinstance(o, list):
            return [convert(v) for v in o]
        if isinstance(o, dict):
            return {k: convert(v) for k, v in o.items()}
        return o

    return convert(dossier)


def test_return_bridge_assumptions_survive_json_round_trip():
    d = make_dossier()
    d.bridge_assumptions.margin_delta_evidenced = True
    d.bridge_assumptions.assumed_margin_delta_cagr = 0.05
    d.bridge_assumptions.margin_delta_mechanism_note = "test mechanism"

    data = _to_plain_json_dict(d)
    reloaded = load_dossier(data)

    assert reloaded.bridge_assumptions.margin_delta_evidenced is True
    assert reloaded.bridge_assumptions.assumed_margin_delta_cagr == 0.05
    assert reloaded.bridge_assumptions.margin_delta_mechanism_note == "test mechanism"


def test_every_stockdossier_field_is_reachable_after_round_trip():
    """Fails loudly if a future field is added to a nested dataclass but the
    loader isn't updated to read it back -- exactly the bug this file exists
    to prevent."""
    d = make_dossier()
    data = _to_plain_json_dict(d)
    reloaded = load_dossier(data)
    assert asdict(reloaded) == asdict(d)
