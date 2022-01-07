import abc

from django.db.models import QuerySet, Q
from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnList


def get_represent_list_data(instance, request: Request, *args, **kwargs) -> ReturnList:
    service_result = instance.service(instance).get_list(request, *args, **kwargs)

    serializer_class = instance.get_serializer_action("list")
    data = serializer_class(service_result, many=True).data
    return data


def get_represent_retrieve_data(instance, request: Request, *args, **kwargs) -> ReturnList:
    service_result = instance.service(instance).get_retrieve(request, *args, **kwargs)

    serializer_class = instance.get_serializer_action("retrieve")
    data = serializer_class(service_result).data
    return data


def get_represent_action_data(instance, **kwargs) -> ReturnList:
    data = instance.service(instance).course_action_service(**kwargs)
    data = instance.get_serializer_class()(data, many=True).data
    return data


class BaseService(metaclass=abc.ABCMeta):
    def __init__(self, instance):
        self.instance = instance

    @abc.abstractmethod
    def get_list(self, request: Request, *args, **kwargs) -> QuerySet:
        pass

    @abc.abstractmethod
    def get_retrieve(self, request: Request, *args, **kwargs) -> QuerySet:
        pass

    @staticmethod
    def _user_filter(request: Request) -> Q:
        return Q(student__user=request.user) | Q(teacher__user=request.user)

    @staticmethod
    def _teacher_filter(request: Request) -> Q:
        return Q(teacher__user=request.user)
