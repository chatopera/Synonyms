__all__ = ["seg",
    "nearby", 
    "compare", 
    "display", 
    "KeyedVectors", 
    "any2utf8",
    "sigmoid",
    "cosine",
    "any2unicode",
    "__version__"]

from .word2vec import *
from .synonyms import *
import jieba
from .synonyms import __version__