from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from .models import Prediction
from .serializers import PredictionSerializer, RegisterSerializer
from .predict_onnx import predict_image


@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Registered"})
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_view(request):
    file = request.FILES['image']

    path = default_storage.save('temp.jpg', file)
    full_path = default_storage.path(path)

    result, confidence = predict_image(full_path)

    Prediction.objects.create(
        user=request.user,
        image=file,
        result=result,
        confidence=confidence
    )

    return Response({
        "result": result,
        "confidence": confidence
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_view(request):
    data = Prediction.objects.filter(user=request.user)
    serializer = PredictionSerializer(data, many=True)
    return Response(serializer.data)