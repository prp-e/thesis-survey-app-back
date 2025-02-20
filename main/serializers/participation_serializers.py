from django.db.models import fields
from rest_framework import serializers
from main.models import (
    ParticipantTeamMember,
    TeamMemberVoiceEvaluationByParticipant,
    GeneralSurveyResponse,
    TeamCoordinationSurveyResponse,
    OverconfidenceSurveyResponse,
)
from hashid_field.rest import HashidSerializerCharField


class ParticipantTeamMemberSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField()

    class Meta:
        model = ParticipantTeamMember
        fields = ["id", "name"]


class VoiceEvaluationSerializer(serializers.ModelSerializer):
    evaluated_participant = ParticipantTeamMemberSerializer()
    # id = HashidSerializerCharField(read_only=True)

    class Meta:
        model = TeamMemberVoiceEvaluationByParticipant
        exclude = ["team", "evaluating_participant"]


class GeneralSurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSurveyResponse
        exclude = ["participant"]


class TeamCoordinationSurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamCoordinationSurveyResponse
        exclude = ["participant"]


class OverconfidenceSurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverconfidenceSurveyResponse
        exclude = ["participant"]


class TeamMemberParticipationSerializer(serializers.ModelSerializer):
    voice_survey_responses = VoiceEvaluationSerializer(many=True)
    general_survey_response = GeneralSurveyResponseSerializer()
    overconfidence_survey_response = OverconfidenceSurveyResponseSerializer()
    team_coordination_survey_response = TeamCoordinationSurveyResponseSerializer()

    id = HashidSerializerCharField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = ParticipantTeamMember
        exclude = ["organization", "team", "has_participated"]
        depth = 2

    def update(self, instance, validated_data):
        if instance.has_participated:
            raise serializers.ValidationError("Already participated")
        voice_survey_responses = validated_data.get("voice_survey_responses")
        for voice_survey_response in voice_survey_responses:
            evaluated_participant_data = voice_survey_response.pop(
                "evaluated_participant"
            )
            evaluated_participant = ParticipantTeamMember.objects.get(
                pk=evaluated_participant_data.get("id")
            )
            TeamMemberVoiceEvaluationByParticipant.objects.create(
                evaluating_participant=instance,
                team=instance.team,
                evaluated_participant=evaluated_participant,
                **voice_survey_response
            )
        GeneralSurveyResponse.objects.create(
            participant=instance, **validated_data.get("general_survey_response")
        )
        OverconfidenceSurveyResponse.objects.create(
            participant=instance, **validated_data.get("overconfidence_survey_response")
        )
        TeamCoordinationSurveyResponse.objects.create(
            participant=instance,
            **validated_data.get("team_coordination_survey_response")
        )
        instance.has_participated = True
        instance.save()
        return instance
