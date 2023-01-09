from board.models import Board
from member.models import Member


from rest_framework.response import Response
from .serializers import BoardSerializer
from rest_framework import viewsets
from rest_framework.decorators import action

class BoardListAPI(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    existQueryset = Board.objects.filter(is_delete='0')

    #[post] /board
    def perform_create(self, serializer):
        user=Member.objects.get(id=self.request.session['id'])
        serializer.save(user=user)

    #[delete] board/{key}
    def perform_destroy(self, instance):
        instance.is_delete = '1'
        instance.save()

    #게시판 반환 , 이때 조회수 +1 처리
    #[get] board/{key}
    def retrieve(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.views=instance.views+1
        instance.save()
        serializer=self.get_serializer(instance)
        return Response(serializer.data)

    #해당 유저가 작성한 게시판 목록 반환
    #[get] board/personal_board
    @action(detail=False,methods=['GET'])
    def personal_board(self,request):
        user = Member.objects.get(id=self.request.session['id'])
        user_board=self.existQueryset.filter(user=user)

        serializer=self.get_serializer(user_board,many=True)
        return Response(serializer.data)

    # [get] board/like_board
    @action(detail=False,methods=['GET'])
    def like_board(self,request):
        like_board=self.existQueryset.order_by('-like')

        serializer = self.get_serializer(like_board, many=True)
        return Response(serializer.data)

    # [get] board/view_board
    @action(detail=False,methods=['GET'])
    def view_board(self,request):
        view_board=self.existQueryset.order_by('-views')

        serializer = self.get_serializer(view_board, many=True)
        return Response(serializer.data)

    # [get] board/date_board
    @action(detail=False, methods=['GET'])
    def date_board(self,request):
        date_board = self.existQueryset.order_by('-date')

        serializer = self.get_serializer(date_board, many=True)
        return Response(serializer.data)