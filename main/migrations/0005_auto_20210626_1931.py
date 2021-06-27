# Generated by Django 3.2.4 on 2021-06-26 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210625_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalsurveyresponse',
            name='participant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='general_survey_response', to='main.participantteammember'),
        ),
        migrations.AlterField(
            model_name='overconfidencesurveyresponse',
            name='participant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='overconfidence_survey_response', to='main.participantteammember'),
        ),
        migrations.AlterField(
            model_name='teamcoordinationsurveyresponse',
            name='participant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='team_coordination_survey_response', to='main.participantteammember'),
        ),
        migrations.AlterField(
            model_name='teammembervoiceevaluationbyparticipant',
            name='evaluating_participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='voice_survey_responses', to='main.participantteammember'),
        ),
    ]
