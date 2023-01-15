from rest_framework import serializers

from nation.models import Nation

class NationSerializer(serializers.ModelSerializer):

  class Meta: 
      model = Nation
      fields = ('nationId','lonlats')