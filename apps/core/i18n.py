import os
from fluent.runtime import FluentBundle, FluentResource

class BackendI18n:
    _bundles = {}

    @classmethod
    def get_bundle(cls, locale):
        if locale not in cls._bundles:
            path = f"bot/locales/{locale}/messages.ftl"
            if not os.path.exists(path):
                # Fallback to en if locale doesn't exist
                if locale == 'en': return None
                return cls.get_bundle('en')

            with open(path, "r", encoding="utf-8") as f:
                resource = FluentResource(f.read())

            bundle = FluentBundle([locale])
            bundle.add_resource(resource)
            cls._bundles[locale] = bundle

        return cls._bundles[locale]

    @classmethod
    def t(cls, locale, key, **kwargs):
        bundle = cls.get_bundle(locale)
        if not bundle:
            return key

        message = bundle.get_message(key)
        if not message or not message.value:
            # Fallback to en bundle if key not found in current locale
            if locale != 'en':
                return cls.t('en', key, **kwargs)
            return key

        pattern = message.value
        res, errors = bundle.format_pattern(pattern, kwargs)
        return res
