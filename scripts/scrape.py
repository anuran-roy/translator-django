from wikipediaapi import Wikipedia

# from asgiref.sync import async_to_sync

# @async_to_sync
# async
def scrape_summary(title: str = "") -> str:
    """
    Scrape Wikipedia summary using ``wikipediaapi.Wikipedia``
    """
    try:
        wiki_obj = Wikipedia().page(title)

        return wiki_obj.summary
    except Exception as e:
        print(e)
        return "ERROR!"
