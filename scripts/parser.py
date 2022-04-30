from typing import List, Dict, Optional, Tuple
import pysbd

# from asgiref.sync import async_to_sync

# @async_to_sync
# async
def parse(to_parse: str = "", lang: str = "") -> List[str]:
    """
    Parses the given strings into multiple strings.
    """
    try:
        segmented_data: List[str] = pysbd.Segmenter(language=lang, clean=False).segment(
            to_parse
        )

        return segmented_data
    except Exception as e:
        print(e)
        return "ERROR!"
