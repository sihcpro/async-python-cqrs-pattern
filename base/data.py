from pyrsistent import PClass
from system.cfg import config


class PayloadData(PClass):
    @classmethod
    def create(
        cls, kwargs, _factory_fields=None, ignore_extra=config.IGNORE_EXTRA_FIELDS,
    ) -> PClass:
        return super().create(
            kwargs, _factory_fields=_factory_fields, ignore_extra=ignore_extra
        )

    @classmethod
    def extend_pclass(
        cls,
        pclass,
        _factory_fields=None,
        ignore_extra=config.IGNORE_EXTRA_FIELDS,
        **kwargs
    ) -> PClass:
        data = (
            pclass.serialize()
            if isinstance(pclass, PClass)
            else pclass
            if pclass
            else dict()
        )

        data.update(kwargs)
        return cls.create(
            data, _factory_fields=_factory_fields, ignore_extra=ignore_extra
        )
