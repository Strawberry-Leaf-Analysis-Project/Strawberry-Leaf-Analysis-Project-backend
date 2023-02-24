import datetime, os

from django.core.files.base import ContentFile

import static.strawberry
import static.txt_to_seperate
import static.leaf_vision
import static.classification_leaves

import cv2
from skimage import io
from board.models import Board
from member.models import Member
from plants_group.models import PlantsGroup
from plants_detail.models import PlantsDetail
from board_like_by_user.models import BoardLikeByUser
from plants_detail.views import PlantsDetailListAPI
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework.response import Response
from .serializers import BoardSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import action

#mask_rcnn=static.strawberry.segmentation("static/mask_rcnn_balloon_0010.h5")
leaf_classification = static.classification_leaves.Load_ResNet_Model("static/leaf_classification_model.pth")

class BoardListAPI(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    existQueryset = Board.objects.filter(is_delete='0')

    #작물 그룹을 어떤걸로 넘겨줄지 의논이 필요함(id 또는 이름) 현재 코드는 이름을 받는걸로
    #[post] /board
    def perform_create(self, serializer):
        user=Member.objects.get(id=self.request.session['id'])
        group=PlantsGroup.objects.get(user=user,name=self.request.data['group_name'])
        group.board_cnt = group.board_cnt + 1
        group.save()
        serializer.save(user=user,plant_group=group)

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

        user = Member.objects.get(id=request.session['id'])
        user_like = BoardLikeByUser.objects.filter(board=instance, member=user,is_delete='0')

        if len(user_like) == 0:
            likes = 0
        else:
            likes = 1

        serializer =self.get_serializer(instance)
        response=Response({'is_like':likes,'data':serializer.data},status=status.HTTP_200_OK)

        if request.COOKIES.get('hit') is not None:
            cookies=request.COOKIES.get('hit')
            cookies_list=cookies.split('|')
            if str(pk) not in cookies_list:
                with transaction.atomic():
                    instance.views+=1
                    instance.save()
                serializer = self.get_serializer(instance)
                response = Response({'is_like':likes,'data':serializer.data}, status=status.HTTP_200_OK)
                response.set_cookie('hit', cookies + f'|{pk}', expires=expires)
        else:
            instance.views+=1
            instance.save()
            serializer = self.get_serializer(instance)
            response = Response({'is_like':likes,'data':serializer.data}, status=status.HTTP_200_OK)
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
        like_board=self.existQueryset.order_by('-likes')

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
        try :
            user = Member.objects.get(id=request.session['id'])
            group = PlantsGroup.objects.get(name=request.data['group_name'])
            board=Board.objects.get(user=user,title__exact=None,plant_group=group)
        except Board.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            self.perform_create(serializer)
            return Response(serializer.data)
        input_file_path = 'media/image/{0}/{1}/{2}/'.format(board.user.id, board.plant_group.name, board.plant_group.board_cnt)
        os.remove(os.path.join(input_file_path, 'input_image.jpg'))
        os.remove(os.path.join(input_file_path, 'output_image.jpg'))
        os.remove(os.path.join(input_file_path, 'leaves_information.txt'))

        board.input_image = request.data['input_image']
        board.save()
        serializer = self.get_serializer(data=board)
        serializer.is_valid()
        return Response(serializer.data)

    # input_image 함수에서 반환해준 id를 전달받는다는 가정하에 진행함
    @action(detail=False,methods=['POST'])
    def output_image(self,request):
        #아래 필터 걸때 user도 같이 걸어야할듯
        user=Member.objects.get(id=request.session['id'])
        group=PlantsGroup.objects.get(name=request.data['group_name'])
        board = Board.objects.get(title__exact=None,user=user,plant_group=group)
        input_file_path = 'media/image/{0}/{1}/{2}/'.format(board.user.id, board.plant_group.name, board.plant_group.board_cnt)
        # 파일명:input_image.jpg

        # output_img=static.strawberry.segmentation(weights,input_file_path)
        mask_rcnn = static.strawberry.segmentation("static/mask_rcnn_balloon_0010.h5")
        output_img, state = static.strawberry.detect_and_color_splash(mask_rcnn, input_file_path) #status 변수 추가해 이벤트 컨트롤
        if state == 0:
            board.output_image=board.input_image
            board.save()

            open(os.path.join(input_file_path,'output_image.jpg'),'w')
            open(os.path.join(input_file_path,'leaves_information.txt'),'w')

            return Response({"success":"fail","msg":"잎이 감지되지 않습니다."})
        output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
        #user = Member.objects.get(id=request.data['id'])

        os.remove(os.path.join(input_file_path,'output_image.jpg'))
        ret, buf = cv2.imencode('.jpg', output_img)
        content = ContentFile(buf.tobytes())

        board.output_image.save('output_image.jpg',content)

        serializer = self.get_serializer(board)

        return Response(serializer.data)

    #게시판의 최종 저장 및 이파리 별 저장(이전 의논 B part 가 돌아갈 함수)
    @action(detail=False, methods=['POST'])
    def write_board(self, request):
        context={}
        board = Board.objects.get(id=request.data['id'])
        board.title=request.data['title']
        board.explain=request.data['explain']

        input_file_path = 'media/image/{0}/{1}/{2}/'.format(board.user.id, board.plant_group.name, board.plant_group.board_cnt)
        # 파일명:input_image.jpg
        N = static.txt_to_seperate.txt_to_seperate(input_file_path)
        board.leaf_cnt=N
        board.save()

        # 각 이파리별로 상태를 0, 1로 나타낸다
        classification_result = static.classification_leaves.classification(leaf_classification, N, input_file_path)

        for i in range(N):
            leaf_path = os.path.join(input_file_path, "leaf_{0}.jpg".format(i + 1))
            leaf_image = io.imread(leaf_path)
            leaf = cv2.cvtColor(leaf_image, cv2.COLOR_BGR2RGB)

            if classification_result[i] == 0 :
                context['state']='0'
            else:
                context['state']='1'

            os.remove(leaf_path)
            leaf = cv2.cvtColor(leaf, cv2.COLOR_BGR2RGB)
            ret, buf = cv2.imencode('.jpg', leaf)
            content = ContentFile(buf.tobytes())

            p_detail = PlantsDetail()
            p_detail.board=board
            p_detail.is_disease=context['state']
            p_detail.leaf_image.save("leaf_{0}.jpg".format(i + 1), content)
            p_detail.save()
        #이파리 판단 함수(여기서 detail 데베를 저장하는것을 동시에 해야할듯)
        #pSerializer=PlantsDetailListAPI.get_serializer(p_detail)
        return Response()

    @action(detail=True, methods=['PATCH'])
    def push_like(self, request, pk=None):
        board = self.existQueryset.get(id=pk)
        user = Member.objects.get(id=request.session['id'])
        is_pushed=request.data['is_pushed']

        if is_pushed == '0':
            board.likes=board.likes+1
            m_likes=BoardLikeByUser.objects.filter(board=board, member=user)

            if len(m_likes) ==0:
                likes=BoardLikeByUser(board=board, member=user)
            else:
                likes=BoardLikeByUser.objects.get(board=board, member=user)
                likes.is_delete='0'
        else:
            board.likes=board.likes-1
            likes=BoardLikeByUser.objects.get(board=board, member=user)
            likes.is_delete='1'

        likes.save()
        board.save()

        serializer = self.get_serializer(board)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def group_board_list(self, request):
        name=request.query_params.get('name')
        user = Member.objects.get(id=request.session['id'])
        group = PlantsGroup.objects.get(name=name,user=user)

        group_name_list = self.existQueryset.filter(plant_group=group)

        serializer = self.get_serializer(group_name_list, many=True)

        return Response(serializer.data)