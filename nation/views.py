from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from nation.models import Nation
from nation.serializers import NationSerializer

from pyproj import Proj, transform

class NationView(ListCreateAPIView):
    model = Nation
    serializer_class = NationSerializer

    def get_queryset(self):
      return Nation.objects.all()

    def utm2lonlat(self, d, i, j, zone):
      srcProj = Proj(proj="utm", zone=zone, ellps="clrk66", units="m")
      dstProj = Proj(proj='longlat', ellps='WGS84', datum='WGS84')
      lonlat = transform(srcProj, dstProj, d * j, d * i)
      return lonlat

    def create(self, request, *args, **kwargs):
      nationId = request.data['nationId']
      utms = request.data['utms']
      lonlats = []
      for utm in utms:
        newlonlat = [i for i in self.utm2lonlat(1000,utm[0],utm[1],20)]
        lonlats.append(newlonlat)
      data = {
        "nationId" : nationId,
        "lonlats" : lonlats
      }  
      try: 
        nation = Nation.objects.get(nationId=nationId)
        message = 'Update a Nation successful!'
        serializer = NationSerializer(nation,data=data)
      except Nation.DoesNotExist:
        message = 'Create a new Nation successful!'
        serializer = NationSerializer(data=data)

      if serializer.is_valid():
          serializer.save()

          return JsonResponse({
              'message': message
          }, status=status.HTTP_201_CREATED)

      return JsonResponse({
          'message': 'Create/Update a Nation unsuccessful!'
      }, status=status.HTTP_400_BAD_REQUEST)

class RetrieveNationView(RetrieveUpdateDestroyAPIView):
    model = Nation
    serializer_class = NationSerializer

    def retrieve(self, request, *args, **kwargs):

      nationId = kwargs.get('nationId')
      nation = Nation.objects.get(nationId=nationId)
      serializer = NationSerializer(nation)
    
      return JsonResponse(
        serializer.data
        , status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        nation = get_object_or_404(Nation, nationId=kwargs.get('nationId'))
        serializer = NationSerializer(nation, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Update Nation successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Update Nation unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        nation = get_object_or_404(Nation, nationId=kwargs.get('nationId'))
        nation.delete()

        return JsonResponse({
            'message': 'Delete Nation successful!'
        }, status=status.HTTP_200_OK)