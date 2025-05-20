from plone.scale.storage import AnnotationStorage as Base

import logging


logger = logging.getLogger(__name__)


class AnnotationStorage(Base):
    def hash_key(self, **parameters):
        key = super().hash_key(**parameters)
        fieldname = parameters.get("fieldname")
        if fieldname:
            field = getattr(self.context, "image", None)
            if getattr(field, "contentType", None) in ("image/jpeg", "image/png"):
                key = f"{key}-webp"
        logger.debug("hash_key %s %s -> %s", self, parameters, key)
        return key

    def hash(self, **parameters):
        key = super().hash(**parameters)
        fieldname = parameters.get("fieldname")
        if fieldname:
            field = getattr(self.context, "image", None)
            if getattr(field, "contentType", None) in ("image/jpeg", "image/png"):
                key = key + (("_format", "webp"),)
        logger.debug("key %s %s -> %s", self, parameters, key)
        return key

    def unhash(self, hash_key):
        return dict(item for item in hash_key if not item[0].startswith("_"))
