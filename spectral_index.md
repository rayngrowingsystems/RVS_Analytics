## Available Spectral Indices

The following spectral indices from [plantCV](https://plantcv.org/) are currently available in RAYN Vision Analytics. 
Please contact us if you are missing an important index, you want us to add to the list. 

(original list from plantCV documentation is available [HERE](https://plantcv.readthedocs.io/en/stable/spectral_index/))

### ARI

Calculates the Anthocyanin Reflectance Index using reflectance values ([Gitelson et al., 2001](#references)):

```
ARI = (1 / R550) - (1 / R700) 

```

### CRI700

Calculates the Carotenoid Reflectance Index 700 using reflectance values ([Gitelson et al., 2002a](#references)):

```
CRI700 = (1 / R510) - (1 / R700)
```

### EVI

Calculates the Enhanced Vegetation index using reflectance values ([Huete et al., 1997](#references)):

```
EVI = (2.5 * (NIR - RED)) / (1 + NIR + (6 * RED) - (7.5 * BLUE))
```

### GLI

Calculates the Green Leaf index using RGB values ([Louhaichi et al., 2001](#references)):

```
GLI = (2 * GREEN - RED - BLUE) / (2 * GREEN + RED + BLUE)
```

### GDVI

Calculates the Green Difference Vegetation Index using reflectance values ([Sripada et al., 2006](#references)):

```
GDVI = (NIR - GREEN) / (NIR + GREEN)
```

### MARI

Calculates the Modified Anthocyanin Reflectance Index using reflectance values ([Gitelson et al., 2006](#references)):

```
MARI = ((1 / R550) - (1 / R700)) * R800
```

### MCARI

Calculates the Modified Chlorophyll Absorption Reflectance Index using reflectance values ([Daughtry et al., 2000](#references)):

```
MCARI = ((R700 - R670) - 0.2 * (R700 - R550)) * (R700 / R670)
```

### NDVI

Calculates the Normalized Difference Vegetation Index using reflectance values ([Rouse et al., 1974](#references)):

```
NDVI = (NIR - RED) / (NIR + RED)
```
  
### PRI

Calculates the Photochemical Reflectance Index using reflectance values ([Penuelas et al., 1995a](#references)):

```
PRI = (R531 - R570) / (R531 + R570)
```

### PSND-Chlorophyll a

Calculates the Pigment Specific Normalized Difference for Chlorophyll a using reflectance values 
([Blackburn 1998](#references)):

```
PSND_CHLA = (R800 - R680) / (R800 + R680)
```

### PSND-Chlorophyll b

Calculates the Pigment Specific Normalized Difference for Chlorophyll b using reflectance values 
([Blackburn 1998](#references)):

```
PSND_CHLB = (R800 - R635) / (R800 + R635)
```

### PSND-Caroteniods

Calculates the Pigment Specific Normalized Difference for Caroteniods using reflectance values 
([Blackburn 1998](#references)):

```
PSND_CAR = (R800 - R470) / (R800 + R470)
```

### PSRI

Calculates the Plant Senescence Reflectance Index using reflectance values ([Merzlyak et al., 1999](#references)):

```
PSRI = (R678 - R500) / R750
```

### PSSR-Chlorophyll a

Calculates the Pigment Specific Simple Ratio for Chlorophyll a using reflectance values 
([Blackburn 1998](#references)):

```
PSSR_CHLA = R800 / R680
```

### PSSR-Chlorophyll b

Calculates the Pigment Specific Simple Ratio for Chlorophyll b using reflectance values 
([Blackburn 1998](#references)):

```
PSSR_CHLB = R800 / R635
```

### PSSR-Caroteniods

Calculates the Pigment Specific Simple Ratio for Caroteniods using reflectance values 
([Blackburn 1998](#references)):

```
PSSR_CAR = R800 / R470
```

### RGRI

Calculates the Red:Green Ratio Index for anthocyanin using reflectance values ([Gamon and Surfus 1999](#references)):

```
RGRI = RED / GREEN
```

### SAVI

Calculates the Soil Adjusted Vegetation Index using reflectance values ([Huete 1988](#references)):

```
SAVI = (1.5 * (NIR - RED)) / (NIR + RED + 0.5)
```

### SIPI

Calculates the Structure-Independent Pigment Index using reflectance values ([Penuelas et al., 1995b](#references)):

```
SIPI = (NIR - RED) / (NIR - BLUE)
```

### SR

Calculates the Simple Ratio using reflectance values ([Jordan 1969](#references)):

```
SR = NIR / RED
```

### References

Barnes EM, Clarke TR, Richards SE, Colaizzi PD, Haberland J, Kostrzewski M, Waller P, Choi C, Riley E, Thompson T, 
Others. 2000. Coincident detection of crop water stress, nitrogen status and canopy density using ground based 
multispectral data. In: Proceedings of the Fifth International Conference on Precision Agriculture, Bloomington, MN, 
USA. [LINK](https://naldc.nal.usda.gov/download/4190/PDF)

Blackburn GA. 1998. Quantifying chlorophylls and caroteniods at leaf and canopy scales: An evaluation of some 
hyperspectral approaches. Remote Sensing of Environment 66:273–285. DOI: 
[10.1016/S0034-4257(98)00059-5](https://doi.org/10.1016/S0034-4257(98)00059-5).

Daughtry CST, Walthall CL, Kim MS, de Colstoun EB, McMurtrey JE. 2000. Estimating corn leaf chlorophyll concentration 
from leaf and canopy reflectance. Remote Sensing of Environment 74:229–239. DOI: 
[10.1016/S0034-4257(00)00113-9](https://doi.org/10.1016/S0034-4257(00)00113-9).

Dash J, Curran PJ. 2004. The MERIS terrestrial chlorophyll index. International Journal of Remote Sensing 25:5403–5413. 
DOI: [10.1080/0143116042000274015](https://doi.org/10.1080/0143116042000274015).

Gamon JA, Surfus JS. 1999. Assessing leaf pigment content and activity with a reflectometer. The New Phytologist 
143:105–117. DOI: [10.1046/j.1469-8137.1999.00424.x](https://doi.org/10.1046/j.1469-8137.1999.00424.x).

Gitelson AA, Zur Y, Chivkunova OB, Merzlyak MN. 2002. Assessing carotenoid content in plant leaves with reflectance 
spectroscopy. Photochemistry and Photobiology 75:272–281. DOI: 
[10.1562/0031-8655(2002)0750272ACCIPL2.0.CO2](https://doi.org/10.1562/0031-8655(2002)0750272ACCIPL2.0.CO2).

Gitelson AA, Kaufman YJ, Stark R, Rundquist D. 2002. Novel algorithms for remote estimation of vegetation fraction. 
Remote Sensing of Environment 80:76–87. DOI: [10.1016/S0034-4257(01)00289-9](https://doi.org/10.1016/S0034-4257(01)00289-9).

Gitelson AA, Viña A, Arkebauer TJ, Rundquist DC, Keydan G, Leavitt B. 2003. Remote estimation of leaf area index and 
green leaf biomass in maize canopies. Geophysical Research Letters 30. DOI: 
[10.1029/2002GL016450](https://doi.org/10.1029/2002GL016450).

Gitelson AA, Keydan GP, Merzlyak MN. 2006. Three-band model for noninvasive estimation of chlorophyll, carotenoids, and 
anthocyanin contents in higher plant leaves. Geophysical Research Letters 33:239. DOI: 
[10.1029/2006GL026457](https://doi.org/10.1029/2006GL026457).

Gitelson AA, Merzlyak MN, Chivkunova OB. 2007. Optical properties and nondestructive estimation of anthocyanin content 
in plant Leaves. Photochemistry and Photobiology 74:38–45. DOI: 
[10.1562/0031-8655(2001)0740038OPANEO2.0.CO2](https://doi.org/10.1562/0031-8655(2001)0740038OPANEO2.0.CO2).

Huete AR. 1988. A soil-adjusted vegetation index (SAVI). Remote Sensing of Environment 25:295–309. 
DOI: [10.1016/0034-4257(88)90106-X](https://doi.org/10.1016/0034-4257(88)90106-X).

Huete AR, HuiQing Liu, van Leeuwen WJD. 1997. The use of vegetation indices in forested regions: issues of linearity 
and saturation. In: IGARSS’97. 1997 IEEE International Geoscience and Remote Sensing Symposium Proceedings. Remote 
Sensing - A Scientific Vision for Sustainable Development. 1966–1968 vol.4. DOI: 
[10.1109/IGARSS.1997.609169](https://doi.org/10.1109/IGARSS.1997.609169).

Jordan CF. 1969. Derivation of leaf-area index from quality of light on the forest floor. Ecology 50:663–666. DOI: 
[10.2307/1936256](https://doi.org/10.2307/1936256).

Louhaichi, M., Borman, M.M., Johnson, D.E., 2001. Spatially Located Platform and Aerial
Photography for Documentation of Grazing Impacts on Wheat. Geocarto International, Volume 16(1), pp. 65–70. DOI: 
[10.1080/10106040108542184](https://doi.org/10.1080/10106040108542184)

Merton R, Huntington J. 1999. Early simulation results of the ARIES-1 satellite sensor for multi-temporal vegetation 
research derived from AVIRIS. [LINK](https://aviris.jpl.nasa.gov/proceedings/workshops/99_docs/41.pdf).

Merzlyak MN, Gitelson AA, Chivkunova OB, Rakitin VYU. 1999. Non-destructive optical detection of pigment changes during 
leaf senescence and fruit ripening. Physiologia Plantarum 106:135–141. DOI: 
[10.1034/j.1399-3054.1999.106119.x](https://doi.org/10.1034/j.1399-3054.1999.106119.x).

Penuelas, J., Gamon, J.A., Fredeen, A.L., Merino, J., Field, C.B., 1994. Reflectance
indices associated with physiological changes in nitrogen and water limited
sunflower leaves. Remote Sensing of Environment 48 (2), 135–146. DOI:
[10.1016/0034-4257(94)90136-8](https://doi.org/10.1016/0034-4257(94)90136-8)

Penuelas J, Filella I, Gamon JA. 1995. Assessment of photosynthetic radiation-use efficiency with spectral reflectance. 
The New Phytologist 131:291–296. DOI: 
[10.1111/j.1469-8137.1995.tb03064.x](https://doi.org/10.1111/j.1469-8137.1995.tb03064.x).

Penuelas J, Baret F, Filella I. 1995. Semi-empirical indices to assess carotenoids/chlorophyll-a ratio from leaf 
spectral reflectance. Photosynthetica 31:221–230. [LINK](https://www.researchgate.net/publication/229084513_Semi-Empirical_Indices_to_Assess_CarotenoidsChlorophyll-a_Ratio_from_Leaf_Spectral_Reflectance).

Penuelas J, Pinol J, Ogaya R, Filella I. 1997. Estimation of plant water concentration by the reflectance Water Index 
WI (R900/R970). International Journal of Remote Sensing 18:2869–2875. DOI: [10.1080/014311697217396](https://doi.org/10.1080/014311697217396).

Rouse JW, Haas RH, Scheel JA, Deering DW. 1974. Monitoring Vegetation Systems in the Great Plains with ERTS. In: 
Freden SC, Mercanti EP, Becker MA eds. Third Earth Resources Technology Satellite-1 Symposium: The Proceedings of a 
Symposium Held by Goddard Space Flight Center at Washington, D.C. on December 10-14, 1973 : Prepared at Goddard Space 
Flight Center. Scientific and Technical Information Office, National Aeronautics and Space Administration, 48–62. 
[LINK](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19740022592.pdf).

Sripada RP, Heiniger RW, White JG, Meijer AD. 2006. Aerial Color Infrared Photography for Determining Early In-Season 
Nitrogen Requirements in Corn. Agronomy Journal 98:968–977. DOI: 
[10.2134/agronj2005.0200](https://doi.org/10.2134/agronj2005.0200).

Woebbecke DM, Meyer GE, Von Bargen K, Mortensen DA. 1995. Color indices for weed identification under various 
soil, residue, and lighting conditions. Transactions of the ASAE. American Society of Agricultural Engineers 38:259–269.
DOI: [10.13031/2013.27838](https://doi.org/10.13031/2013.27838).
