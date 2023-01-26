import datetime, os

from board.models import Board
from member.models import Member
from plants_group.models import PlantsGroup
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from .serializers import BoardSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import action

class BoardListAPI(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    existQueryset = Board.objects.filter(is_delete='0')

    #작물 그룹을 어떤걸로 넘겨줄지 의논이 필요함(id 또는 이름) 현재 코드는 이름을 받는걸로
    #[post] /board
    def perform_create(self, serializer):
        user=Member.objects.get(id=self.request.session['id'])
        group=PlantsGroup.objects.get(user=user,name=self.request.data['group_name'])
        user.board_cnt = user.board_cnt + 1
        user.save()
        serializer.save(user=user,plant_group=group)
        #
        #
        #
        #output
        #board.get id,

    #[delete] board/{key}
    def perform_destroy(self, instance):
        instance.is_delete = '1'
        instance.save()

    #게시판 반환 , 이때 조회수 +1 처리
    #[get] board/{key}
    def retrieve(self, request, pk=None):
        instance=get_object_or_404(self.existQueryset,pk=pk)
        tomorrow=datetime.datetime.replace(timezone.datetime.now(),hour=23,minute=59,second=0)
        expires=datetime.datetime.strftime(tomorrow,"%a, %d-%b-%Y %H:%M:%S KST")

        serializer =self.get_serializer(instance)
        response=Response(serializer.data,status=status.HTTP_200_OK)

        if request.COOKIES.get('hit') is not None:
            cookies=request.COOKIES.get('hit')
            cookies_list=cookies.split('|')
            if str(pk) not in cookies_list:
                with transaction.atomic():
                    instance.views+=1
                    instance.save()
                serializer = self.get_serializer(instance)
                response = Response(serializer.data, status=status.HTTP_200_OK)
                response.set_cookie('hit', cookies + f'|{pk}', expires=expires)
        else:
            instance.views+=1
            instance.save()
            serializer = self.get_serializer(instance)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            response.set_cookie('hit', pk, expires=expires)

        return response


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

    # [get] board/search
    @action(detail=False, methods=['GET'])
    def search(self,request):
        data=request.query_params.get('search')

        search_user=Member.objects.filter(id__icontains=data)
        search_board = self.existQueryset.filter(title__icontains=data)

        for user in search_user:
            search_board=search_board|self.existQueryset.filter(user=user)

        serializer = self.get_serializer(search_board, many=True)

        return Response(serializer.data)

    # [patch] board/{key}/change_board/?title={}&explain={}
    # 유저 비번 바꾸는거랑 동일한 방식으로 보내면 됨
    @action(detail=True,methods=['PATCH'])
    def change_board(self,request,pk=None):
        board=self.existQueryset.get(id=pk)
        title=request.data['title']
        explain=request.data['explain']

        if title=='':
            return Response({"message":"제목을 입력해주세요"})

        if explain=='':
            return Response({"message": "내용을 입력해주세요"})

        board.title=title
        board.explain=explain
        board.save()

        serializer=self.get_serializer(board)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def input_image(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        self.perform_create(serializer)
        return Response(serializer.data)

    # input_image 함수에서 반환해준 id를 전달받는다는 가정하에 진행함
    @action(detail=False,methods=['POST'])
    def output_image(self,request):
        board=Board.objects.get(id=request.data['id'])
        input_file_path='media/image/{0}/{1}/{2}/'.format(board.user.id,board.plant_group.name,board.user.board_cnt)
        #파일명:input_image.jpg
        print(input_file_path)
        #이후 세그멘테이션 함수를 넣어 진행하면될듯 여기서 함수 반환값을 박싱된 이미지를 주면 될듯
        #segment_func():이 함수에서 이파리 좌표값 넣은 텍스트파일(?)은 알아서 저장해야할듯?

        #opencvimage to PILIMage and save output_image(fileField)
        #board.save()
        return Response()


    #게시판의 최종 저장 및 이파리 별 저장(이전 의논 B part 가 돌아갈 함수)
    @action(detail=False, methods=['POST'])
    def write_board(self, request):
        board = Board.objects.get(id=request.data['id'])
        input_file_path = 'media/image/{0}/{1}/{2}/'.format(board.user.id, board.plant_group.name, board.user.board_cnt)
        # 파일명:input_image.jpg
        #잎의 개수를 게시판 데베에 저장
        #이파리 판단 함수(여기서 detail 데베를 저장하는것을 동시에 해야할듯)

        return Response()


