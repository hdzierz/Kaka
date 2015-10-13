from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import *

from .logger import *
from .django_ext import *
from .models_base import *

import datetime


class MouseIntakeOb(Ob):
    unit = models.ForeignKey(Unit)
    biosubject = models.ForeignKey(BioSubject, null=True, blank=True)
    descriptor = models.CharField(max_length=255, default="")
    age = models.IntegerField(default=0)
    diet = models.ForeignKey(Diet, null=True)
    intake = models.FloatField(default=None, null=True)
    comment = models.CharField(max_length=255, default="")

    @staticmethod
    def Clean(datasource):
        MouseIntakeOb.objects.filter(datasource=datasource).delete()


class MouseWeightOb(Ob):
    unit = models.ForeignKey(Unit)
    biosubject = models.ForeignKey(BioSubject, null=True, blank=True)
    descriptor = models.CharField(max_length=255, default="")
    age = models.IntegerField(default=0)
    diet = models.ForeignKey(Diet, null=True)
    weight = models.FloatField(default=None, null=True)
    comment = models.CharField(max_length=255, default="")

    @staticmethod
    def Clean(datasource):
        MouseWeightOb.objects.filter(datasource=datasource).delete()


class MouseHistologyOb(Ob):
    unit = models.ForeignKey(Unit)
    biosample = models.ForeignKey(BioSample)
    biosubject = models.ForeignKey(BioSubject, null=True, blank=True)
    descriptor = models.CharField(max_length=255, default="")
    week = models.IntegerField(default=0)
    diet = models.ForeignKey(Diet, null=True)
    inflam_type = models.CharField(max_length=255, default="unknown")
    sub_type = models.CharField(max_length=255, default="=unknown")
    score = models.FloatField(default=None, null=True)
    adj_score = models.FloatField(default=None, null=True)
    comments = models.CharField(max_length=1024, default="")

    @staticmethod
    def Clean(datasource):
        MouseHistologyOb.objects.filter(datasource=datasource).delete()


class MouseHistologyV2Ob(Ob):
    biosample = models.ForeignKey(BioSample)
    biosubject = models.ForeignKey(BioSubject, null=True, blank=True)
    scorer = models.CharField(max_length=20, default="unknown")
    diet = models.ForeignKey(Diet, null=True)
    crypt_hyperplasia = models.IntegerField(default=None, null=True)
    aberrant_crypts = models.IntegerField(default=None, null=True)
    crypt_injury = models.IntegerField(default=None, null=True)
    crypt_loss = models.IntegerField(default=None, null=True)
    goblet_cell_loss = models.IntegerField(default=None, null=True)
    crypt_abscess = models.IntegerField(default=None, null=True)
    lymphoid_aggregates = models.IntegerField(default=None, null=True)
    submucosal_thickening = models.IntegerField(default=None, null=True)
    hyperchromatic = models.IntegerField(default=None, null=True)
    surface_loss = models.IntegerField(default=None, null=True)
    monocytes_and_macrophages = models.IntegerField(default=None, null=True)
    neutrophils = models.IntegerField(default=None, null=True)
    plasma_cells_and_lymphocytes = models.IntegerField(default=None, null=True)
    muscular_layer = models.IntegerField(default=None, null=True)
    omental_fat = models.IntegerField(default=None, null=True)
    all_unit = models.ForeignKey(Unit, null=True, related_name='all_unit')
    comments = models.CharField(max_length=1024, default="")

    @staticmethod
    def Clean(datasource):
        MouseHistologyV2Ob.objects.filter(datasource=datasource).delete()


class EpigeneticsOb(Ob):
    unit = models.ForeignKey(Unit)
    biosample = models.ForeignKey(BioSample)
    biosubject = models.ForeignKey(BioSubject, null=True, blank=True)
    island = models.CharField(max_length=255, default="CpG_unkown")
    methylation = models.FloatField(null=True)
    assay = models.CharField(max_length=255, default="-9999")
    diet = models.CharField(max_length=255, default="")
    lid = models.CharField(max_length=255, default="")
    descriptor = models.CharField(max_length=255, default="")
    week = models.IntegerField(null=True)

    @staticmethod
    def Clean(datasource):
        EpigeneticsOb.objects.filter(datasource=datasource).delete()


class ProteinGelSpotOb(Ob):
    biosample = models.ForeignKey(BioSample)
    biosubject = models.ForeignKey(BioSubject, null=True, blank=True)
    fold_change = models.FloatField(null=True)
    num_uniq_pep = models.IntegerField(null=True)
    spot_no = models.CharField(max_length=155, default="unkown")
    acc_num = models.CharField(max_length=255, null=True)
    gene_mgi = models.CharField(max_length=255, null=True)
    prot_ident = models.CharField(max_length=255, null=True)
    theo_pl = models.FloatField(null=True)
    sequest_p = models.FloatField(null=True)
    spot = models.IntegerField(null=True)
    seq_cov = models.FloatField(null=True)
    theo_al = models.FloatField(null=True)
    M_Gel = models.CharField(max_length=255, default="-9999")
    descriptor = models.CharField(max_length=255, default="")
    week = models.IntegerField(null=True)
    file_name = models.CharField(max_length=1024, default="")

    @staticmethod
    def Clean(datasource):
        ProteinGelSpotOb.objects.filter(datasource=datasource).delete()



class QuestionnaireOb(Ob):
    debug = False
    biosubject = models.ForeignKey(BioSubject, null=True, blank=True)
    att_key = models.CharField(max_length=255)
    att_value = models.CharField(max_length=4096, default=None, null=True)
    att_code = models.CharField(max_length=255, default=None, null=True)
    grp = models.CharField(max_length=1024, default="")

    @staticmethod
    def SaveOb(study, biosubject, key, value, grp=-9999):
        if(QuestionnaireOb.debug):
            Logger.Error(value)
        riob = QuestionnaireOb()
        riob.att_key = key
        riob.att_value = value
        riob.study = study
        riob.biosubject = biosubject
        riob.save()

    @staticmethod
    def GetOb(study, biosubject, key, grp=-9999):
        ob = QuestionnaireOb.objects.get(
            study=study,
            biosubject=biosubject,
            att_key=key,
            grp=grp
            )
        if(ob):
            return ob.att_value
        else:
            Logger.Warning(
                "Ob.GetOb: Key does not exist: {0}/{1}".format(
                    ob.xreflsid,
                    key
                    )
                )
            return None

    @staticmethod
    def GetObs(study, biosubject=None):
        grps = QuestionnaireOb.objects.filter(
            study=study).order_by("grp").distinct("grp")
        res = []
        for grp in grps:
            if(biosubject):
                ris = QuestionnaireOb.objects.filter(
                    study=study,
                    biosubject=biosubject,
                    grp=grp.grp
                    )
            else:
                ris = QuestionnaireOb.objects.filter(study=study, grp=grp.grp)

            v = {}
            for r in ris:
                v[r.att_key] = r.att_value
            res.append(v)
        if(QuestionnaireOb.debug):
            Logger.Message(str(res))
        return res


class Genotype(Category):
    typ = models.CharField(max_length=255, default="SNP")


class GenotypeOb(Ob):
    biosubject = models.ForeignKey(BioSubject)
    genotype = models.ForeignKey(Genotype)
    observationdate = models.DateField(null=True)
    genotypeobserved = models.CharField(max_length=255, default=None, null=True)
    genotypeobserved_comment = models.CharField(
        max_length=1024,
        default="",
        null=True
        )
    finalgenotype = models.CharField(max_length=255, default=None, null=True)
    finalgenotype_comment = models.CharField(
        max_length=1024,
        default="",
        null=True
        )


class GenotypeObLg(models.Model):
    biosubject = models.ForeignKey(BioSubject)
    study = models.ForeignKey(Study)
    genotype = models.ForeignKey(Genotype)
    genotypeobserved = models.CharField(max_length=10, default=None, null=True)
    datasource = models.ForeignKey(DataSource)

    class Meta(Ob.Meta):
        managed = False
        db_table = 'api_genotypeob_lg'

