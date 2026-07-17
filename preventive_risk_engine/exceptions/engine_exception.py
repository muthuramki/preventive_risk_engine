class EngineError(Exception):
    """Base class for all engine-level errors.

    Per Section 13 ('Safe failure'): callers must fail toward 'needs review',
    never toward a falsely low/reassuring score. Catch this at the pipeline
    boundary and route to manual review rather than suppressing it silently.
    """
