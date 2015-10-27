from seafood.models import *

def run():
    onto = Ontology.objects.get(name="Term")
    ds, ceated = DataSource.objects.get_or_create(name = "Loading Fish Scores", ontology=onto, supplier="Seafood")

    Term.objects.all().delete()

    fs = Term()
    fs.datasource = ds
    fs.group = 'Fin score'
    fs.name = 'damage severity tearing'
    fs.values = {'slight': 1, 'moderate': 2, 'significant': 3, 'major': 4}
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'Fin score'
    fs.name = 'damage severity bruising'
    fs.values = {'slight': 1, 'moderate': 2, 'major': 3}
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'External Twitch'    
    fs.name = 'yes no'
    fs.values = { 'yes': 1, 'no': 0 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'External Twitch'
    fs.name = 'Twitch Whole Body'
    fs.values = { 'minor': 8, 'moderate': 16, 'major': 24 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'External Twitch'
    fs.name = 'Twitch Half Body'
    fs.values = { 'minor': 7, 'moderate': 15, 'major': 23 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'External Twitch'
    fs.name = 'Twitch Fins'
    fs.values = { 'minor': 6, 'moderate': 14, 'major': 22 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'External Twitch'
    fs.name = 'Twitch Gill/Jaw'
    fs.values = { 'minor': 5, 'moderate': 13, 'major': 21 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS eye score'
    fs.name = 'Left Eye Too Damaged'
    fs.values = { 'yes': 12, 'no': 0 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS eye score'
    fs.name = 'Left Eye Cornea Colour'
    fs.values = { 'clear': 0, 'transluscent': 1, 'milky': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS eye score'
    fs.name = 'Left Eye Pupil Colour'
    fs.values = { 'black': 0, 'dull black': 1, 'grey': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS eye score'
    fs.name = 'Left Eye Form'
    fs.values = { 'convex': 0, 'flat': 1, 'sunken': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS eye score'
    fs.name = 'Left Eye Cold/Osmotic'
    fs.values = { 'no cold damage': 0, 'minor cold damage': 1, 'major cold damage': 2, 'osmotic damage': 1 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS eye score'
    fs.name = 'Left Eye Bleeding'
    fs.values = { 'none': 0, 'minor bleeding': 1, 'moderate bleeding': 1.5, 'major bleeding': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS eye score'
    fs.name = 'Left Eye Bubbles'
    fs.values = { 'none': 0, 'present': 1 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS eye score'
    fs.name = 'Left Eye Bulging'
    fs.values = { 'no': 0, 'yes': 1 }
    fs.save()

###########################################

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS eye score'
    fs.name = 'Right Eye Too Damaged'
    fs.values = { 'yes': 12, 'no': 0 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS eye score'
    fs.name = 'Right Eye Cornea Colour'
    fs.values = { 'clear': 0, 'transluscent': 1, 'milky': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS eye score'
    fs.name = 'Right Eye Pupil Colour'
    fs.values = { 'black': 0, 'dull black': 1, 'grey': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS eye score'
    fs.name = 'Right Eye Form'
    fs.values = { 'convex': 0, 'flat': 1, 'sunken': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS eye score'
    fs.name = 'Right Eye Cold/Osmotic'
    fs.values = { 'no cold damage': 0, 'minor cold damage': 1, 'major cold damage': 2, 'osmotic damage': 1 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS eye score'
    fs.name = 'Right Eye Bleeding'
    fs.values = { 'none': 0, 'minor bleeding': 1, 'moderate bleeding': 1.5, 'major bleeding': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS eye score'
    fs.name = 'Right Eye Bubbles'
    fs.values = { 'none': 0, 'present': 1 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS eye score'
    fs.name = 'Right Eye Bulging'
    fs.values = { 'no': 0, 'yes': 1 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS Fillet score'
    fs.name = 'yes no'
    fs.values = { 'no': 0, 'yes': 1 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS Fillet score'
    fs.name = 'intensity'
    fs.values = { 'slight': 0, 'moderate': 1, 'extensive': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS Fillet score'
    fs.name = 'yes no'
    fs.values = { 'no': 0, 'yes': 1 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS Fillet score'
    fs.name = 'intensity'
    fs.values = { 'slight': 0, 'moderate': 1, 'extensive': 2 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS Internal Twitch'
    fs.name = 'Twitch Whole Fillet'
    fs.values = { 'minor': 4, 'moderate': 10, 'major': 20 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS Internal Twitch'
    fs.name = 'Twitch Half Fillet'
    fs.values = { 'minor': 3, 'moderate': 11, 'major': 19 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS Internal Twitch'
    fs.name = 'Twitch Belly'
    fs.values = { 'minor': 2, 'moderate': 10, 'major': 18 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'LHS Internal Twitch'
    fs.name = 'Twitch Tail'
    fs.values = { 'minor': 1, 'moderate': 9, 'major': 17 }
    fs.save()

###############################

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS Internal Twitch'
    fs.name = 'Twitch Whole Fillet'
    fs.values = { 'minor': 4, 'moderate': 10, 'major': 20 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS Internal Twitch'
    fs.name = 'Twitch Half Fillet'
    fs.values = { 'minor': 3, 'moderate': 11, 'major': 19 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS Internal Twitch'
    fs.name = 'Twitch Belly'
    fs.values = { 'minor': 2, 'moderate': 10, 'major': 18 }
    fs.save()

    fs = Term()
    fs.datasource = ds
    fs.group = 'RHS Internal Twitch'
    fs.name = 'Twitch Tail'
    fs.values = { 'minor': 1, 'moderate': 9, 'major': 17 }
    fs.save()




