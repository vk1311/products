"""Template registry: (file slug, builder function, one-line description)."""

from .templates_a import TEMPLATES_A
from .templates_b import TEMPLATES_B
from .templates_c import TEMPLATES_C

REGISTRY = TEMPLATES_A + TEMPLATES_B + TEMPLATES_C
