# Wikichip scraper

In progress, is for [SpecDB](https://specdb.info/) so they're not stuck manually entering data.

Why did I make this its own seperate repo rather than a fork? IDK.

You need BS4, this can be installed with `pip install beautifulsoup4`

If SpecDB ever included ECC memory support the scraper has this information as
'has ecc memory support'

## TODO:
* include XFR stat
* Change frequencies to GHz - Done, but need to check if any other needs to be changed.
* include Chipsets in the inherit
* Allow the user to start the scraping process at a different stage. - Done, but notify user on whats missing by doing this.
* Make starting file(ie. Vermeer.yaml (vermeer-inherit and the vermeer folder gets made.)) HALF DONE
  * list of sockets for main file
  * earliest release date
  * Lithography
  * directX and vulkan support if APU/
* categorise CPUs into their categories (CPU-SERVER, CPU-DESKTOP, APU-DESKTOP ect) STARTED
* Sometimes wikichip will append "Socket" to the start of a socket. So rather than "AM4" it will say "Socket AM4"
* When scraping Vermeer, the scraper will put Unlocked: false in the inherit, when it should be true...
* When scraping Vermeer, The main file normally starts with ryzen 9, then 7, then 5. The scraper will just put it in as it gets it and thats usually ryzen 9, then 7 then 5.

* APU specs
  * For APU data, html.find('span',{'id':'Graphics'}) on individual APU page.
  * Though techpowerup like https://www.techpowerup.com/gpu-specs/radeon-graphics-384sp-mobile.c3856 seems to work better.
  * in general, APU specs being
    * GPU Model
    * GPU Base Frequency
    * Max Displays
    * Shader processor Count
    * Texture mapping unit count
    * Render output unit count
    * VRAM type
    * Crossfire Support
    
