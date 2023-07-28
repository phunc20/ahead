from __future__ import annotations
from pathlib import Path

import FlowCal


def get_fsc_ssc_chunks(
    fcs_file: str | Path,
    *,
    chunk_size: int = 500,
    typ: str = "A",
    gate_fraction: float = 0.0,
):
    channels = [f'FSC-{typ}', f'SSC-{typ}']
    s = FlowCal.io.FCSData(str(fcs_file))
    s = FlowCal.transform.to_rfi(s)
    s_gated = FlowCal.gate.high_low(
        s,
        channels=channels,
    )
    if 0 < gate_fraction <= 1:
        s_gated = FlowCal.gate.density2d(
            s_gated,
            channels=channels,
            gate_fraction=gate_fraction,
        )
    n_events = s_gated.shape[0]
    for k in range(0, n_events, chunk_size):
        chunk = s_gated[k:k+chunk_size, channels]
        yield chunk







