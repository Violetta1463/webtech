from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Entry
from .serializers import EntrySerializer
from .permissions import IsOwnerOrReadOnly
class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsOwnerOrReadOnly]
    search_fields = ['name','message']
    ordering_fields = ['created_at','name']
    ordering = ['-created_at']
    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        qs = Entry.objects.filter(user=request.user).order_by('-created_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        return Response(self.get_serializer(qs, many=True).data)
