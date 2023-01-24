from disease.models import Disease

from rest_framework.response import Response
from .serializers import DiseaseSerializer
from rest_framework import viewsets

class DiseaseListAPI(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

    #필요인자:name:질병명
    #[post] /disease/
    def create(self, request):
        exist = self.queryset.filter(name=request.data['name'])  # id 중복 검사

        if len(exist) != 0:
            return Response({"message": "해당 질병은 이미 등록되어 있습니다."})

        serializer = self.get_serializer(data=request.data)  # 요청값->serializer

        if serializer.is_valid():  # 입력값이 serializer에서 설정한 유효성 검사를 통과했다면
            serializer.save()  # 저장,is_valid 호출후 사용가능
            return Response(serializer.data)  # 해당값을 반환해줌 보내줌
        return Response(serializer.error)  # is_valid 호출후에 사용가능

    # 삭제 처리 안됨
    #[delete] /disease/{id}
    def perform_destroy(self, instance):
        #instance.is_delete = '1'
        instance.save()


