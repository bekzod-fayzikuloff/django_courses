def get_comments(instance, pk=None):
    score = instance.queryset.filter(pk=pk).first()
    comments = instance.get_queryset().filter(score=score)
    comments = instance.get_serializer_class()(comments, many=True)
    return comments
