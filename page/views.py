from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from rest_framework import status

@api_view(['GET', 'POST', 'DELETE'])
def notes_view(request):
    if request.method == 'GET':
        # 處理 GET 請求
        notes = Note.objects.all()
        data = [{'id': note.id, 'note': note.note, 'created_at': note.created_at} for note in notes]
        return Response(data)

    elif request.method == 'POST':
        # 處理 POST 請求
        note_content = request.data.get('note')
        if note_content:
            note = Note.objects.create(note=note_content)
            return Response({
                'id': note.id,
                'note': note.note,
                'created_at': note.created_at
            }, status=status.HTTP_201_CREATED)
        return Response({'error': 'No note content provided'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # 處理 DELETE 請求，支援一次刪除多筆
        note_ids = request.data.get('ids')  # 期望接收一個 id 列表
        if note_ids:
            # 嘗試刪除符合 id 的筆記
            notes_to_delete = Note.objects.filter(id__in=note_ids)
            if notes_to_delete.exists():
                notes_to_delete.delete()
                return Response({'message': f'{len(note_ids)} notes deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'No notes found with the provided IDs'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'No note IDs provided'}, status=status.HTTP_400_BAD_REQUEST)


