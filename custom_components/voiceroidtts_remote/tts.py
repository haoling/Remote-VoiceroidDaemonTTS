import logging

import asyncio
import aiohttp
import re
import async_timeout
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.tts import CONF_LANG, PLATFORM_SCHEMA, Provider
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from urllib.parse import quote

from . import DEFAULT_LANG


_LOGGER = logging.getLogger(__name__)

SUPPORT_LANGUAGES = ["aoi-narrator", "aoi", "akane", "akari"]

CONF_URL = "url"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_URL): cv.string,
        vol.Optional(CONF_LANG, default=DEFAULT_LANG): vol.In(SUPPORT_LANGUAGES)
    }
)


def get_engine(hass, config, discovery_info=None):
    return VoiceroidProvider(hass, config[CONF_URL], config[CONF_LANG])


class VoiceroidProvider(Provider):
    def __init__(self, hass, url, language):
        self._hass = hass
        self._url = url
        self._language = language
        self.name = "VoiceroidTTS ({})".format(self._language)

    @property
    def default_language(self):
        """Return the default language."""
        return self._language

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    async def async_get_tts_audio(self, message, language, options=None):
        """Load TTS using a remote pico2wave server."""
        websession = async_get_clientsession(self._hass)

        try:
            with async_timeout.timeout(5):
                url_param = {
                    "who": language,
                    "text": message,
                }

                request = await websession.get(self._url, params=url_param)

                if request.status != 200:
                    _LOGGER.error(
                        "Error %d on load url %s", request.status, request.url
                    )
                    return (None, None)
                data = await request.read()

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for PicoTTS API")
            return (None, None)

        if data:
            return ("wav", data)
        return (None, None)
