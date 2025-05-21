from plone.scale.storage import AnnotationStorage as Base

import logging


logger = logging.getLogger(__name__)


class AnnotationStorage(Base):
    def hash_key(self, **parameters):
        fieldname = parameters.get("fieldname")
        if fieldname:
            field = getattr(self.context, fieldname, None)
            if getattr(field, "contentType", None) in ("image/jpeg", "image/png"):
                force_webp = True
        key = super().hash_key(**parameters)
        if force_webp:
            key += "-webp"  # XXX: visibile utile per debugging
        return key

    def hash(self, **parameters):
        fieldname = parameters.get("fieldname")
        if fieldname:
            field = getattr(self.context, fieldname, None)
            if getattr(field, "contentType", None) in ("image/jpeg", "image/png"):
                # XXX: hack per fozare la conversione anche quando non ci sarebbe necessità
                #      di fare uno scale
                parameters["convert_to_webp"] = True
        key = super().hash(**parameters)
        return key
