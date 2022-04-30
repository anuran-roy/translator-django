from typing import Optional, Dict, List, Tuple
import urllib
import requests
import json
import os

# from asgiref.sync import async_to_sync

# @async_to_sync
# async
def use_google_translate(src: str = "", to: str = "", sentence: str = "") -> str:
    """
    Uses the Google Translate API in the RapidAPI Marketplace to request the translated version of a sentence using Google Translate, into a particular language.

    API Docs at: [**Google Translate - RapidAPI MarketPlace**](https://rapidapi.com/googlecloud/api/google-translate1/)
    """
    API_URL: str = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    query_string: str = urllib.parse.quote(sentence)

    payload: str = f"q={query_string}&target={to}&source={src}"

    headers: Dict[str, str] = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
        "X-RapidAPI-Key": os.environ.get("GOOGLE_TRANSLATE_API_KEY"),
    }
    response_data: Dict[str, any] = {}
    try:
        response_data = requests.request(
            "POST", API_URL, data=payload, headers=headers
        ).json()

        translated_text: str = ""
        translated_text = response_data["data"]["translations"][0]["translatedText"]
        # print(translated_text)
        return translated_text

    except KeyError:
        print(response_data["message"])
        print("ERROR! Monthly limit reached!")
        return "ERROR!"
    except Exception as e:
        print(e)
        return "ERROR!"


def use_just_translated(src: str = "", to: str = "", sentence: str = "") -> str:
    """
    Uses the Just Translated API in the RapidAPI marketplace.

    API Docs at: [**Just Translated - RapidAPI MarketPlace**](https://rapidapi.com/lebedev.str/api/just-translated/)
    """
    API_URL = "https://just-translated.p.rapidapi.com/"

    querystring = {"lang": f"{src}-{to}", "text": sentence}

    headers = {
        "X-RapidAPI-Host": "just-translated.p.rapidapi.com",
        "X-RapidAPI-Key": os.environ.get("JUST_TRANSLATED_API_KEY"),
    }

    response: Dict[str, any] = {}

    try:
        response = requests.request("GET", API_URL, headers=headers, params=querystring)

        # print(response.text)
        return json.loads(response.text)["text"][0]
    except KeyError:
        print(response["message"])
        print("ERROR! Monthly limit reached!")
        return "ERROR!"
    except Exception as e:
        print(e)
        return "ERROR!"


def detect_language(sentence: str) -> str:
    pass
