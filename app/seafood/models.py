from django.db import models
#from django.db.models.signals import pre_save
#from django.dispatch import receiver
#from django.core.exceptions import ObjectDoesNotExist
from djangotoolbox.fields import DictField, EmbeddedModelField
from django_countries.fields import CountryField
from django.db.models.base import *
from jsonfield import JSONField

from api.logger import *
from api.django_ext import *
from api.models import *


class City(Feature):
    pass


class Vessel(Feature):
    pass


class Crew(Feature):
    pass


class Tree(Feature):
    pass


class Trip(Feature):
    def __unicode__(self):
        return self.name


class Staff(Feature):
    status = models.CharField(max_length=255)
    initials = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Tow(Feature):
    trip = models.ForeignKey(Trip)

    values = JSONField()


class Fish(Feature):
    form_completed = models.BooleanField(default=False)
    trip = models.ForeignKey(Trip)
    tow = models.ForeignKey(Tow)

    def __unicode__(self):
        return str(self.GetName())

    def save(self, *args, **kwargs):
        #self.calc_external_twitch(self)
        #self.calc_fin_score(self)
        #self.calc_lhs_eye_score(self)
        #self.calc_rhs_eye_score(self)
        #self.calc_lhs_fillet_score(self)
        #self.calc_rhs_fillet_score(self)
        #self.calc_lhs_torry_avg(self)
        #self.calc_rhs_torry_avg(self)
        #self.calc_lhs_internal_twitch(self)
        #self.calc_rhs_internal_twitch(self)
        super(Fish, self).save(*args, **kwargs)

    def GetName(self):
        try:
            return self.study.name + '.' + self.trip.name + '.' + str(self.name)
        except:
            return 'unknown_study.unknown_trip.' + str(self.name)

    def GetColumns(self):
        try:
            return list(self.values.keys())
        except:
            return ()

    def GetValuesAsDict(self):
        return dict(self.values)

    class Meta(Ob.Meta):
        pass


    def calc_external_twitch(self, ob):
        twitch_intensity = GetKV(ob, 'Twitch Intensity')
            
        targets = ['Twitch Whole Body', 'Twitch Half Body', 'Twitch Fins', 'Twitch Gill/Jaw']

        res = 0

        for target in targets:
            try:
                yn = GetKV(ob, target)
                if(yn.lower() == 'yes'):
                    vfbo = Term.objects.get(Q(group='External Twitch') & Q(name=target))
                    vfb = vfbo.values[twitch_intensity.lower()]
                    res += vfb
            except:
                pass

        SaveKV(ob, 'External Twitch', str(res)) 
        return res


    def calc_fin_score(self, ob):
        targets_tearing = [
            'Left Pectoral Fin Tearing', 
            'Left Pelvic Fin Tearing', 
            'Tail Fin Tearing',
            'Anal Fin Tearing',
            'Dorsal Fin Tearing',
            'Right Pectoral Fin Tearing',
            'Right Pelvic Fin Tearing',
        ]

        targets_bruising = [
            'Left Pectoral Fin Bruising',
            'Left Pelvic Fin Bruising',
            'Tail Fin Bruising',
            'Anal Fin Bruising',
            'Dorsal Fin Bruising',
            'Right Pectoral Fin Bruising',
            'Right Pelvic Fin Bruising',
        ]

        res = 0

        for target in targets_tearing:
            try:
                score = Term.objects.get(Q(group='Fin score') & Q(name='damage severity tearing'))
                score_category = GetKV(ob, target)
    
                if score_category.lower() in score.values:            
                    score = score.values[score_category.lower()]
                else:
                    score = 0
                res += score
            except:
                pass

        for target in targets_bruising:
            try:
                score = Term.objects.get(Q(group='Fin score') & Q(name='damage severity bruising'))
                score_category = GetKV(ob, target)
                if score_category.lower() in score.values:
                    score = score.values[score_category.lower()]
                else:
                    score = 0
                res += score
            except:
                pass

        SaveKV(ob, 'Fin score', str(res))
        return res


    def calc_lhs_eye_score(self, ob):
        scores = Term.objects.filter(group='LHS eye score')
        res = 0

        for score in scores:
            val = GetKV(ob, score.name)
            if val.lower() in score.values:
                sc = score.values[val.lower()]
            else:
                sc = 0
            res += sc
            
        SaveKV(ob, 'LHS eye score', str(res))
        return res


    def calc_rhs_eye_score(self, ob):
        scores = Term.objects.filter(group='RHS eye score')
        res = 0

        for score in scores:
            try:
                val = GetKV(ob, score.name)
                if val.lower() in score.values:
                    sc = score.values[val.lower()]
                else:
                    sc = 0
                res += sc
            except:
                pass

        SaveKV(ob, 'RHS eye score', str(res))
        return res


    def calc_lhs_fillet_score(self, ob):
        scores = Term.objects.get(Q(group='LHS Fillet score') & Q(name='yes no'))
        targets = [
                    'Left Blood Spot A',
                    'Left Blood Spot B',
                    'Left Blood Spot C',
                    'Left Blood Spot D',
                    'Left Blood Spot E',
                    'Left Blood Spot F',
                    'Left Blood Spot G',
                    'Left Blood Spot H',
            ]

        res = 0

        for bloodspot in targets:
            try:
                val = GetKV(ob, bloodspot.name)
                if val in scores.values:
                    sc = scores.values[val]
                else:
                    sc = 0
                res += sc
            except:
                pass


        scores = Term.objects.get(Q(group='LHS Fillet score') & Q(name='intensity'))
        targets = [
                'Left Gaping V2',
                'Left Gaping V1',
                'Left Gaping D1',
                'Left Gaping D2',
                'Left Gaping D3',
                'Left Gaping D3D2',
                'Left Gaping D2D1',
                'Left Gaping D1V1',
                'Left Gaping V1V2',
        ]   

        for gaping in targets:
            val = GetKV(ob, gaping)
            if val.lower() in scores.values:
                sc = scores.values[val.lower()]
            else:
                sc = 0
            res += sc

        SaveKV(ob, 'LHS Fillet score', str(res))
        return res


    def calc_rhs_fillet_score(self, ob):
        scores = Term.objects.get(Q(group='RHS Fillet score') & Q(name='yes no'))
        targets = [
                    'Right Blood Spot A',
                    'Right Blood Spot B',
                    'Right Blood Spot C',
                    'Right Blood Spot D',
                    'Right Blood Spot E',
                    'Right Blood Spot F',
                    'Right Blood Spot G',
                    'Right Blood Spot H',
            ]

        res = 0

        scores = Term.objects.get(Q(group='RHS Fillet score') & Q(name='intensity'))

        for bloodspot in targets:
            try:
                val = GetKV(ob, bloodspot)
                if val.lower() in scores.values:
                    sc = scores.values[val.lower()]
                else:
                    sc = 0
                res += sc
            except:
                pass

        targets = [
            'Right Gaping V2',
            'Right Gaping V1',
            'Right Gaping D1',
            'Right Gaping D2',
            'Right Gaping D3',
            'Right Gaping D3D2',
            'Right Gaping D2D1',
            'Right Gaping D1V1',
            'Right Gaping V1V2',

        ]

        for gaping in targets:
            val = GetKV(ob, gaping)
            if val.lower() in scores.values:
                sc = scores.values[val.lower()]
            else:
                sc = 0
            res += sc

        SaveKV(ob, 'RHS Fillet score', str(res))
        return res


    def calc_lhs_torry_avg(self, ob):
        targets = [
            'Left Fillet Torry 1',
            'Left Fillet Torry 2',
            'Left Fillet Torry 3',
        ]

        res = 0
        for target in targets:
            val = GetKV(ob, target)
            if val:
                res += float(val)/len(targets)

        SaveKV(ob, 'Left Torry Avg', str(res))
        return res


    def calc_rhs_torry_avg(self, ob):
        targets = [
            'Right Fillet Torry 1',
            'Right Fillet Torry 2',
            'Right Fillet Torry 3',
        ]

        res = 0
        for target in targets:
            val = GetKV(ob, target)
            if val:
                res += float(val)/len(targets)

        SaveKV(ob, 'Right Torry Avg', str(res))
        return res


    def calc_lhs_internal_twitch(self, ob):
        fillet_twitch_intensity = GetKV(ob, 'Left Fillet Twitch Intensity')
        fillet_twitch_location = GetKV(ob, 'Left Fillet Twitch Location')

        res = 0

        if(fillet_twitch_intensity and fillet_twitch_location):
            try:
                scores = Term.objects.get(Q(name=fillet_twitch_location) & Q(group='LHS Internal Twitch'))
                res += scores.values[fillet_twitch_intensity]
            except:
                pass

        SaveKV(ob, 'Left Fillet Twitch Intensity', str(res))
        return res


    def calc_rhs_internal_twitch(self, ob):
        fillet_twitch_intensity = GetKV(ob, 'Right Fillet Twitch Intensity')
        fillet_twitch_location = GetKV(ob, 'Right Fillet Twitch Location')

        res = 0

        if(fillet_twitch_intensity and fillet_twitch_location):
            try:
                scores = Term.objects.get(Q(name=fillet_twitch_location) & Q(group='RHS Internal Twitch'))
                res += scores.values[fillet_twitch_intensity]
            except:
                pass

        SaveKV(ob, 'Right Fillet Twitch Intensity', str(res))
        return res

    
# SIGNALS
@receiver(pre_save)
def set_calc_fields(sender, instance, **kwargs):
    class_name = instance.__class__.__name__
    try:
        instance.IsOb()
    except Exception:
        return

    try:
        res = {}
        res['External Twitch'] = calc_external_twitch(instance)
        res['Fin Score'] = calc_fin_score(instance)
        
        
        
    except ObjectDoesNotExist:
        msg = "ERROR in signal set_ontology. Uknown class: %s." % class_name
        Logger.Warning(msg)
        raise DataError(msg)


