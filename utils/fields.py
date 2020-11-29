import inspect
import importlib
from rest_framework.fields import Field
from rest_framework.serializers import BaseSerializer


def _signature_parameters(func):
    try:
        inspect.signature()
    except AttributeError:
        return inspect.getargspec(func).args
    else:
        return inspect.signature(func).parameters.keys()

class RecursiveField(Field):
    PROXIED_ATTRS = (
        'get_value',
        'get_initial',
        'run_validation',
        'get_attribute',
        'to_representation',
        'field_name',
        'source',
        'read_only',
        'default',
        'source_attrs',
        'write_only',
    )

    def __init__(self, to=None, **kwargs):
        self.to = to
        self.init_kwargs = kwargs
        self._proxied = None

        super_kwargs = dict(
            (key, kwargs[key])
            for key in kwargs
            if key in _signature_parameters(Field.__init__)
        )
        super(RecursiveField, self).__init__(**super_kwargs)

    def bind(self, field_name, parent):
        self.bind_args = (field_name, parent)

    @property
    def proxied(self):
        if not self._proxied:
            if self.bind_args:
                field_name, parent = self.bind_args
                
                if hasattr(parent, 'child') and parent.child is self:
                    parent_class = parent.parent.__class__
                else:
                    parent_class = parent.__class__
                    
                assert  issubclass(parent_class, BaseSerializer)

                if self.to is None:
                    proxied_class = parent_class
                else:
                    try:
                        module_name, class_name = self.to.rsplit('.', 1)
                    except ValueError:
                        module_name, class_name = parent_class.__module__, self.to

                    try:
                        proxied_class = getattr(
                            importlib.import_module(module_name), class_name)
                    except Exception as e:
                        raise ImportError('could not locate serializer %s' % self.to, e)

                proxied = proxied_class(**self.init_kwargs)
                proxied.bind(field_name, parent)
                self._proxied = proxied

        return self._proxied

    def __getattribute__(self, name):
        if name in RecursiveField.PROXIED_ATTRS:
            try:
                proxied = object.__getattribute__(self, 'proxied')
                return getattr(proxied, name)
            except AttributeError:
                pass
        return object.__getattribute__(self, name)
