from django.shortcuts import render, redirect
from csgames_quals import models


def index(request):
    participants = models.Participant.objects.all()
    for participant in participants:
        participant.score = 0
        for competition in participant.competitions.all():
            if competition in participant.preferences.all():
                participant.score += 1


    competitions = models.Competition.objects.all()
    return render(request, 'index.html', {'participants': participants, 'competitions': competitions})


def participant_details(request, id):
    participant = models.Participant.objects.get(pk=id)
    preferences = participant.preferences.all()
    competitions = participant.competitions.all()
    return render(request, 'participant.html', {'participant': participant, 'preferences': preferences,
                                                'competitions': competitions})


def competition_details(request, id, warning=None):
    competition = models.Competition.objects.get(pk=id)
    participants = competition.participants.all()
    n_places = 3 - len(participants)

    participants_list = models.Participant.objects.all()
    pref_list = []
    for participant in participants_list:
        prefs = list(participant.preferences.all())
        if competition in prefs:
            pref_list.insert(prefs.index(competition), participant)

    return render(request, 'competition.html', {'competition': competition,
                                                'participants': participants,
                                                'n_places': n_places,
                                                'participants_list': participants_list,
                                                'pref_list': pref_list,
                                                'warning': warning})


def assign_participant(request, competition_id, participant_id):
    warning = ''
    competition = models.Competition.objects.get(pk=competition_id)
    participant = models.Participant.objects.get(pk=participant_id)

    if participant in competition.participants.all():
        competition.participants.remove(participant)
    else:
        if len(competition.participants.all()) < 3:
            for comp in participant.competitions.all():
                if comp.date == competition.date and comp.time == competition.time:
                    warning += 'Conflit d\'horraire !<br>'
                    break
            competition.participants.add(participant)
        if len(participant.competitions.all() )> 4:
            warning += 'Ce participant a plus de 4 competitions !<br>'
        if competition not in participant.preferences.all():
            warning += 'Ce participant n\'a pas cette competition dans ces preferences<br>'

    competition.save()
    return competition_details(request, competition.id, warning)


def schedule(request):
    participants = models.Participant.objects.all()
    competitions = models.Competition.objects.all()

    conflicts = []
    for participant in participants:
        for comp in participant.competitions.all():
            for comp_temp in participant.competitions.all():
                if comp != comp_temp:
                    if comp.date == comp_temp.date and comp.time == comp_temp.time:
                        conflicts.append(participant.name + ' est en conflit d\'horraire ' + comp.date + ' ' + comp.time)


    noobs = []
    for participant in participants:
        if len(participant.competitions.all()) < 3:
            noobs.append(participant)

    warnings = []
    for participant in participants:
        for competition in participant.competitions.all():
            if competition not in participant.preferences.all():
                warnings.append({'participant': participant, 'competition': competition})

    schedule_score = 0
    for participant in participants:
        for competition in participant.competitions.all():
            if competition in participant.preferences.all():
                schedule_score += 1

    return render(request, 'schedule.html', {'participants': participants,
                                             'competitions': competitions,
                                             'conflicts': conflicts,
                                             'noobs': noobs,
                                             'warnings': warnings,
                                             'schedule_score': schedule_score})