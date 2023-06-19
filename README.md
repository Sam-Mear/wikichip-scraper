# Wikichip scraper

In progress, is for [SpecDB](https://specdb.info/) so they're not stuck manually entering data.

Why did I make this its own seperate repo rather than a fork? IDK.

You need BS4, this can be installed with `pip install beautifulsoup4`

If SpecDB ever included ECC memory support the scraper has this information as
'has ecc memory support'

## TODO:
* give out a warning/file for cpus with missing specs. DONE
* include XFR stat
* Change frequencies to GHz - Done, but need to check if any other needs to be changed.
* include Chipsets in the inherit
* Allow the user to start the scraping process at a different stage. - But notify user on whats missing by doing this.
* Make starting file(ie. Vermeer.yaml (vermeer-inherit and the vermeer folder gets made.)) HALF DONE
* categorise CPUs into their categories (CPU-SERVER, CPU-DESKTOP, APU-DESKTOP ect) STARTED
* APU specs