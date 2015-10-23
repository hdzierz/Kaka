<style>
.reveal h1, .reveal h2, .reveal h3 {
  word-wrap: normal;
  -moz-hyphens: none;
}
.small-code pre code {
  font-size: 1em;
}
.midcenter {
    position: fixed;
    top: 50%;
    left: 50%;
}
.footer {
    color: black; background: #E8E8E8;
    position: fixed; top: 90%;
    text-align:center; width:100%;
}
.pinky .reveal .state-background {
  background: #FF69B4;
} 
.pinky .reveal h1,
.pinky .reveal h2,
.pinky .reveal p {
  color: black;
}
</style>


Kaka: Towards a Distrubuted Genotype Information System
========================================================
author: Helge Dzierzon Samantha Baldwin
date: October 28 2015


TOC
========================================================

* Why?
* How?
* Status
* Conclusions

Issues by PFR distribution of Wetware
========================================================

* PFR distributed
* Genotype information created
* Nobody knows what others do
* Genotype infomration is produced on a lot of these sites
* Analysts usually somewhere else and needs access to the data
* Data currently spread on K-Drives

***

![PFR](images/pfr_nz.png)

Existing Databases Initiatives in PFR
========================================================

* EBrida (provenance)
* KEA (sample tracking)
* Ensembl

DBs in development
========================================================

* Kaka (Genotypes)
* Kakapo (Location)


Kaka Techniques
========================================================

* Python Django
* PGSQL and JSON
* Docker and continuous integration

***

Python, PgSQL, Docker, Travis


Status
========================================================

* DB has been developed as a proof of concept
* Some example data have been loaded
* RStudio, noteboods databases etc. have been attached and can access api
* API has been developed

***

Screenshot

Conclusions
========================================================

* Concept is simple but a bit nerdy
* It is a great tool already but needs a nerd
* Blubb

Thank you! Questions?
========================================================

Image


