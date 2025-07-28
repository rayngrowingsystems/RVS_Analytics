## Available Spectral Indices

The following spectral indices from [plantCV](https://plantcv.org/) are currently available in RAYN Vision Analytics. 
Please contact us if you are missing an important index, you want us to add to the list.

(Original list from plantCV documentation is available [HERE](https://plantcv.readthedocs.io/en/stable/spectral_index/))

## Wavelength Adaption in RAYN Vision System

Some spectral indices in RAYN Vision Analytics use adjusted wavelengths to match the available bands in our multispectral imaging system. These adaptations are based on literature and spectral similarity and maintain sensitivity for comparative plant studies in controlled environments.

**Substitution: 855 nm instead of 800 nm**
The RVS Camera has two NIR channels: 855 and 950. We use the 855 the channel as standard NIR-band in the indices (if not stated otherwise). Reflectance in the NIR plateau is generally stable across 800–860 nm in healthy vegetation. Substituting 800 nm with 855 nm preserves sensitivity to biomass and canopy structure, especially in relative comparisons.

Supporting literature:
- Gitelson et al. (2003) validated NIR reflectance stability in the 800–860 nm range for biomass estimation. [DOI:10.1029/2002GL016450](#references)
- Barnes et al. (2000) report interchangeable use of NIR bands above 800 nm for water and canopy indices.

**Substitution: 740 nm instead of 700 nm**
Our system uses a band centered at 740 nm to approximate the red edge. The red-edge transition is spectrally smooth between 700–750 nm. Using 740 nm retains chlorophyll sensitivity while improving signal quality.

Supporting literature:
- Gitelson et al. (2003) showed robust vegetation sensitivity across 700–750 nm. DOI:10.1029/2002GL016450
- Dash & Curran (2004) used similar bands in MERIS-based indices. DOI:10.1080/0143116042000274015

**Substitution: 526 nm instead of 550 nm**
Our green channel peaks at 526 nm. While 550 nm is standard for chlorophyll-related indices (e.g. ARI, MARI), 526 nm still lies within the green reflectance plateau and is commonly used in remote sensing sensors like WorldView-2 and RedEdge.

Supporting literature:
- Blackburn (1998) highlights broad sensitivity of chlorophyll in the 520–560 nm region. DOI:10.1016/S0034-4257(98)00059-5
- Gitelson et al. (2006) also report flexibility in green bands for non-invasive pigment estimates. DOI:10.1029/2006GL026457

These adjustments are especially valid in indoor setups with masked plant material, where relative differences between treatments are prioritized over absolute index values.


### ARI

Calculates the Anthocyanin Reflectance Index using reflectance values ([Gitelson et al., 2001](#references)):

```
ARI = (1 / R526) - (1 / R740)
```
**Modified:** R550 → R526 and R700 → R740  
**Reason:** No exact 550 nm or 700 nm bands available. 526 and 740 provide best approximation.

### CI (modified)

Calculates the Chlorophyll Index using reflectance values, adapted from Gitelson et al., 2003.
We use 665 nm (Deep Red) and 855 nm (NIR) instead of the originally suggested 680 nm and 800 nm due to sensor availability.
The substitution preserves the index’s sensitivity to chlorophyll in red-edge and NIR bands.

```
CI = (R855 / R665) - 1
```

### CRI526

Calculates the Carotenoid Reflectance Index 526 using reflectance values ([Gitelson et al., 2002a](#references)):

```
CRI740 = (1 / R500) - (1 / R740)
```
**Modified:** R510 → R500 and R700 → R740  
**Reason:** Nearest matching bands to assess carotenoid reflectance.

### CRI740

Calculates the Carotenoid Reflectance Index 740 (originally 700) using reflectance values ([Gitelson et al., 2002a](#references)):

```
CRI740 = (1 / R500) - (1 / R740)
```
**Modified:** R510 → R500 and R700 → R740  
**Reason:** Nearest matching bands to assess carotenoid reflectance.

### EGI

Calculates the Excess Green Index using RGB values ([Woebbecke et al., 1995](#references)):

```
r = R700 / (R740 + R530 + R460)
g = R530 / (R740 + R530 + R460)
b = R460 / (R740 + R530 + R460)
EGI = 2g - r - b
```
**Note:** With images from the RAYN Vision System Camera the RGB bands are approximated using the available bands: R → R665, G → R526, B → R475

### EVI

Calculates the Enhanced Vegetation index using reflectance values ([Huete et al., 1997](#references)):

```
EVI = (2.5 * (NIR - RED)) / (1 + NIR + (6 * RED) - (7.5 * BLUE))
```
**Note:** With images from the RAYN Vision System Camera the RED and NIR bands are approximated using the available bands: Red → R665, NIR → R855

### GLI

Calculates the Green Leaf index using RGB values ([Louhaichi et al., 2001](#references)):

```
GLI = (2 * GREEN - RED - BLUE) / (2 * GREEN + RED + BLUE)
```
**Note:** With images from the RAYN Vision System Camera the RGB bands are approximated using the available bands: R → R665, G → R526, B → R475

### GDVI

Calculates the Green Difference Vegetation Index using reflectance values ([Sripada et al., 2006](#references)):

```
GDVI = (NIR - GREEN) / (NIR + GREEN)
```
**Note:** With images from the RAYN Vision System Camera the GREEN and NIR bands are approximated using the available bands: Green → R526, NIR → R855

### MARI

Calculates the Modified Anthocyanin Reflectance Index using reflectance values ([Gitelson et al., 2006](#references)):

```
MARI = ((1 / R550) - (1 / R700)) * R800
```
**Modified:** R550 → R526, R700 → R740, R800 → R855

### MCARI

Calculates the Modified Chlorophyll Absorption Reflectance Index using reflectance values ([Daughtry et al., 2000](#references)):

```
MCARI = ((R700 - R670) - 0.2 * (R700 - R550)) * (R700 / R670)
```
**Modified:** R700 → R740, R550 → R526

### NDRE (modified)

Calculates the Normalized Difference Red Edge Index. We use 740 nm and 855 nm instead of 720 nm and 790 nm. This modification remains within the red-edge to NIR transition range, as described in Gitelson et al., 2003, and is suitable for estimating chlorophyll content.
```
NDRE = (R855 - R740) / (R855 + R740)
```

### NDVI

Calculates the Normalized Difference Vegetation Index using reflectance values ([Rouse et al., 1974](#references)):

```
NDVI = (NIR - RED) / (NIR + RED)
```
**Note:** With images from the RAYN Vision System Camera the RED and NIR bands are approximated using the available bands: Red → R665, NIR → R855

### NPCI

Calculates the Normalized Pigment Chlorophyll Index (Penuelas et al., 1995b). We use 665 nm (Deep Red) and 475 nm (Blue) instead of 680 nm and 430 nm due to hardware constraints.
This change slightly shifts the balance toward red-light reflectance but retains the index’s purpose in detecting pigment ratio changes.
```
NPCI = (R665 - R475) / (R665 + R475)
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
**Note:** With images from the RAYN Vision System Camera the GREEN and RED bands are approximated using the available bands: Green → R526, Red → R665

### SAVI

Calculates the Soil Adjusted Vegetation Index using reflectance values ([Huete 1988](#references)):

```
SAVI = (1.5 * (NIR - RED)) / (NIR + RED + 0.5)
```
**Note:** With images from the RAYN Vision System Camera the RED and NIR bands are approximated using the available bands: Red → R665, NIR → R855

### SIPI

Calculates the Structure-Independent Pigment Index using reflectance values ([Penuelas et al., 1995b](#references)):

```
SIPI = (NIR - RED) / (NIR - BLUE)
```
**Note:** With images from the RAYN Vision System Camera the BLUE, RED and NIR bands are approximated using the available bands: Blue → R475, Red → R665, NIR → R855

### SR

Calculates the Simple Ratio using reflectance values ([Jordan 1969](#references)):

```
SR = NIR / RED
```
**Note:** With images from the RAYN Vision System Camera the RED and NIR bands are approximated using the available bands: Red → R665, NIR → R855

### Water Band Index (WBI)
Calculates the Water Band Index, adapted from Penuelas et al., 1997. We use 855 nm and 950 nm instead of the canonical 900 nm and 970 nm. This substitution remains valid for water status estimation, as both bands are within the NIR water absorption region (Gao 1996).
```
WBI = R855 / R950
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
