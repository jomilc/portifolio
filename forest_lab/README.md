# Forest Lab: Forest growth, ecological succession and anthropogenic interference

**Version:** 1.0.0  
**Author:** Jomil Costa Abreu Sales (Sales, J.; C.; A.), Ph.D. in Environmental Sciences, [ORCID 0000-0001-8722-8398](https://orcid.org/0000-0001-8722-8398)  
**DOI:** 10.5281/zenodo.23859145  
**License:** All rights reserved. Viewing and non-commercial academic use with citation are permitted; see `LICENSE.txt`.

Forest Lab is an interactive 3D simulator of tropical forest succession over 1,000 years on a 100-hectare landscape (1,000 m × 1,000 m). It compares a natural riparian edge with two anthropogenic edges (vineyard/agriculture and urban expansion). It also lets users explore forest structure with an emulated airborne LiDAR point cloud. The interface is available in English and Portuguese.

![Forest Lab: 3D forest at year 150](forest_lab_01_forest_3d.png)

## Features

- **Five succession phases (years 0–1,000):**
  - initial creeping grasses (0–3);
  - herbaceous and pioneer expansion (3–15);
  - secondary forest and understory (15–60);
  - late secondary/climax forest (60–150);
  - mature old-growth forest with emergent megatrees (150+).
- **Light-driven succession (see Growth model below):** seven functional groups (pioneers, pioneer shrubs, early and late secondary species, shade-tolerant understory treelets and palms, climax species and emergents) replace each other according to the light that reaches each site. Dead trees never come back: the site is recolonized by new small plants in the successional order. The understory is drawn as low, wide shrubs and small spreading-crown treelets, with small extra clumps around them (visual only).
- **Edge effects:**
  - meandering river with gallery forest (natural edge, about −7% biomass);
  - vineyard/agriculture to the west (about −24% in the contact zone);
  - urban expansion to the east (about −48% in the contact zone).

  Edges reduce growth and raise mortality of large trees (Laurance et al., 2002). Light-demanding pioneers and shrubs persist along the edges.
- **Urban zone detail:** when urban expansion is switched on, the city rises in an animation. It has:
  - a street grid with lane and crosswalk markings;
  - buildings with lit windows;
  - houses with gabled roofs;
  - a factory whose chimneys release smoke that drifts with the wind.

  These elements are visual only; the urban edge-effect calculation is the same.
- **Gap dynamics:** natural treefall gaps (deaths of large trees crush smaller neighbours and open the canopy), plus an interactive tool to open a gap at an emergent tree and follow its recovery. When the user fells a tree, a flock of blue and scarlet macaws flees the crown, a visual reminder of habitat and biodiversity loss.
- **Environmental drivers:** rainfall, soil fertility, gap rate and foliage density. A 6-second rain pulse includes cloud formation and a modest growth boost.
- **Metrics and charts:** all read from the simulated history:
  - 1,000-year evolution of each group;
  - diameter growth (cm/yr) and mortality (%/yr) per group, with a 15-year moving average;
  - canopy cover from the light model;
  - vertical LiDAR profile;
  - maximum height;
  - aboveground biomass (AGB, Mg/ha) from the pantropical allometry of Chave et al. (2014).
- **LiDAR Cloud mode:** a high-density emulated airborne scan (about 420,000 returns). Points can be coloured by species and stems, by height (Z) or by ground/vegetation, on a black background. The legend and colour options open in a collapsible side tab on the left edge. This mode is a simplified in-browser emulation inspired by the HELIOS++ virtual laser scanning approach (Winiwarter et al., 2022). It does not run HELIOS++.
- **Camera presets:** isometric, nadir (ALS), urban edge, rural edge, riparian corridor and understory.
- **Data import:** a JSON file of tree positions and sizes (`dados_floresta_1000anos.json`, for example exported from a Google Colab workflow) can replace the built-in succession model.

## Growth model

Forest Lab uses a simplified individual-based, light-driven gap model, in the spirit of JABOWA (Botkin et al., 1972) and FORMIND (Köhler & Huth, 1998). The 3,300 points of the landscape are sites. Over 1,000 years each site is occupied by successive generations of any functional group.

**Light.** The leaf area of every crown is spread over a 40 m grid and over 5 m height layers, from the crown base to the top. Light below a given height follows the Lambert–Beer law, L = exp(−k · LAI above), with k = 0.5 (Monsi & Saeki, 1953/2005). Light at the forest floor drops to about 3% in the mature forest.

**Recruitment.** An empty site is recolonized according to the light at the ground (facilitation and tolerance; Connell & Slatyer, 1977). Following the "initial floristic composition" pattern (Finegan, 1996), later-successional trees can establish among the pioneers from the first years, but they grow slowly while shaded:

|  #  | Group (example genera)                                   | Enters at          | Ground light | Lifespan (yr) | Max height (m) | Wood density (g/cm³) |
| :-: | -------------------------------------------------------- | ------------------ | :----------: | :-----------: | :------------: | :------------------: |
|  1  | Pioneers (grasses, *Cecropia*, *Trema*)                  | year 0 (seed bank) |    ≥ 28%     |     15–35     |       20       |         0.35         |
|  2  | Pioneer shrubs (*Piper*, *Miconia*, *Vismia*)            | year 2             |    ≥ 15%     |     15–40     |       6        |         0.40         |
|  3  | Early secondary (*Inga*, *Schizolobium*)                 | year 3             |    ≥ 12%     |     40–80     |       26       |         0.52         |
|  4  | Late secondary (*Cedrela*, *Virola*)                     | year 4             |     any      |    100–220    |       34       |         0.65         |
|  5  | Climax (*Carapa*, *Manilkara*, *Hymenaea*)               | year 5             |     any      |    300–600    |       43       |         0.80         |
|  6  | Shade-tolerant treelets and palms (*Euterpe*, *Geonoma*) | year 10            |    ≤ 30%     |     70–140    |       10       |         0.45         |
|  7  | Emergents (*Bertholletia*, *Dinizia*, *Cariniana*)       | year 12            |     any      |    500–900    |       68       |         0.72         |

Groups follow Budowski (1965), Finegan (1996) and Chazdon (2014). Each site has a "home" group (the species pool of the landscape) and is recolonized mostly by it, with a smaller chance for other groups (seed rain). In a gap inside the forest (lit ground, shaded surroundings), direct sun breaks the dormancy of the soil seed bank and pioneers can germinate at any site, producing the colonizer pulse (Finegan, 1996; Denslow, 1987).

**Growth.** Height grows towards the group maximum (monomolecular curve). Growth slows under the shade of taller trees (suppression) and with poor soil or edge stress. Crown radius follows height allometrically. Heights never decrease.

**Pioneers and shrubs persist in full sun.** While a pioneer or pioneer shrub receives at least 70% of full light at its top, it does not die from senescence, background mortality or edge stress. It disappears only when taller trees start to shade it. The only exceptions are physical destruction: a large tree falling on it, a gap opened by the user, or land converted to city or agriculture. In the default run, none of the pioneer or shrub deaths over 1,000 years happens in full sun. The pioneer stand starts to decline at about 20–25 years, when early secondary trees overtop it, and almost disappears by 150 years. It then survives only in gaps and along edges, as described by Denslow (1987) and Laurance et al. (2002).

**Understory under the emergents.** The deep, humid shade below large emergent crowns (> 45 m) is the best habitat for shade-tolerant treelets and palms. Under those crowns they establish three times faster and die about three times less often. About 90 extra understory-only sites lie close to the emergents.

As a result, the mature understory (years 300–1,000) holds about 890 plants instead of about 700 (+25%), with about twice as many plants under each large emergent. It is also steadier: about 1.6% of plants are replaced per year, and the year-to-year change is about 0.5%.

**Mortality (all other cases).**
- Background mortality of 0.4–4% per year, depending on the group and scaled by the "gap rate" slider. Tropical forests turn over at about 1–2% per year (Phillips & Gentry, 1994).
- Senescence at the end of the drawn lifespan.
- Shading of light-demanding groups, which produces self-thinning.
- Photoinhibition of shade-tolerant treelets in large gaps (Denslow, 1987).
- Extra mortality near edges.
- Crushing of smaller neighbours when a large tree falls.

**Biomass.** Each site stands for a cohort of real trees of its group. AGB uses the pantropical allometry of Chave et al. (2014) with a diameter proxy from crown radius.

**Calibration.** The default run reaches:
- about 85 Mg/ha at 60 years, 135 Mg/ha at 100 years and 210 Mg/ha at 150 years;
- about 260–290 Mg/ha in the old-growth forest;
- canopy height of about 32 m at 60 years and 68 m emergents after about 400 years.

These values fall within the ranges reported for Neotropical secondary and old-growth forests (Chave et al., 2014; Poorter et al., 2016). Edge intensities were calibrated so the contact zones lose about 48% (city), 25% (vineyard) and 7% (river) of their biomass.

**Reproducibility.** All random draws come from a fixed-seed hash. Edge intensities were calibrated on the average of 4 independent seeds. The whole 1,000-year history is computed at once (about 0.6–0.7 s on a laptop) and recomputed when a scenario changes. Moving the timeline back and forth always shows the same forest.

![LiDAR point cloud mode](forest_lab_02_lidar_point_cloud.png)

![Urban edge: city next to the forest](forest_lab_03_edge_effect.png)

![Urban zone with factory smoke](forest_lab_04_urban_zone.png)

## How to run

1. Download `forest_lab.html`.
2. Open it in a current browser (Chrome, Edge, Firefox or Safari) with WebGL enabled. It works on computers and on phones:
   - on small screens the layout adapts automatically. A compact ☰ icon menu groups all the controls (strata, land use, sensor, cameras, analysis, author), so the 3D scene stays visible. The playback bar is compact and shrinks to the timeline alone while the simulation plays. Edge-effect notices (river, vineyard, city) are collected in a draggable ⓘ tab instead of pop-ups;
   - landscape orientation is recommended on phones;
   - on touch devices the graphics quality is reduced automatically to keep the animation smooth.
3. Use **Help (❓)** inside the simulator for the full guide. Topic 7 lists the complete references.

Requirements:

- **Internet connection on first load.** The page loads three.js r128 and Tailwind CSS 3.4.17 from public CDNs (cdnjs, jsDelivr and cdn.tailwindcss.com).
- **A dedicated or recent integrated GPU is recommended.** The renderer lowers its resolution automatically on slower machines.

No installation, server or account is needed. All simulation runs locally in the browser, and no data is collected or sent anywhere.

## How to cite

**English:**
SALES, J.; C.; A. Forest Lab: Forest growth, ecological succession and anthropogenic interference. Version 1.0.0. Zenodo, 2026. DOI: 10.5281/zenodo.23859145. Available at: https://orcid.org/0000-0001-8722-8398.

**Portuguese (ABNT):**
SALES, J.; C.; A. Forest Lab: Crescimento florestal, sucessão ecológica e interferência antrópica. Versão 1.0.0. Zenodo, 2026. DOI: 10.5281/zenodo.23859145. Disponível em: https://orcid.org/0000-0001-8722-8398.

**APA:**
Sales, J. C. A. (2026). *Forest Lab: Forest growth, ecological succession and anthropogenic interference* (Version 1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.23859145

**BibTeX:**

```bibtex
@software{sales_2026_forest_lab,
  author    = {Sales, Jomil Costa Abreu},
  title     = {{Forest Lab: Forest growth, ecological succession and anthropogenic interference}},
  year      = 2026,
  publisher = {Zenodo},
  version   = {1.0.0},
  doi       = {10.5281/zenodo.23859145},
  url       = {https://doi.org/10.5281/zenodo.23859145}
}
```

Machine-readable citation metadata is in `CITATION.cff`.

## References

### Scientific literature

1. Botkin, D. B., Janak, J. F., & Wallis, J. R. (1972). Some ecological consequences of a computer model of forest growth. *Journal of Ecology, 60*(3), 849–872. https://doi.org/10.2307/2258570
2. Budowski, G. (1965). Distribution of tropical American rain forest species in the light of successional processes. *Turrialba, 15*(1), 40–42.
3. Chave, J., Réjou-Méchain, M., Búrquez, A., Chidumayo, E., Colgan, M. S., Delitti, W. B. C., Duque, A., Eid, T., Fearnside, P. M., Goodman, R. C., Henry, M., Martínez-Yrízar, A., Mugasha, W. A., Muller-Landau, H. C., Mencuccini, M., Nelson, B. W., Ngomanda, A., Nogueira, E. M., Ortiz-Malavassi, E., Pélissier, R., Ploton, P., Ryan, C. M., Saldarriaga, J. G., & Vieilledent, G. (2014). Improved allometric models to estimate the aboveground biomass of tropical trees. *Global Change Biology, 20*(10), 3177–3190. https://doi.org/10.1111/gcb.12629
4. Chazdon, R. L. (2014). *Second growth: The promise of tropical forest regeneration in an age of deforestation*. University of Chicago Press. ISBN 978-0-226-11807-9.
5. Connell, J. H., & Slatyer, R. O. (1977). Mechanisms of succession in natural communities and their role in community stability and organization. *The American Naturalist, 111*(982), 1119–1144. https://doi.org/10.1086/283241
6. Denslow, J. S. (1987). Tropical rainforest gaps and tree species diversity. *Annual Review of Ecology and Systematics, 18*, 431–451. https://doi.org/10.1146/annurev.es.18.110187.002243
7. Finegan, B. (1996). Pattern and process in neotropical secondary rain forests: The first 100 years of succession. *Trends in Ecology & Evolution, 11*(3), 119–124. https://doi.org/10.1016/0169-5347(96)81090-1
8. Guariguata, M. R., & Ostertag, R. (2001). Neotropical secondary forest succession: Changes in structural and functional characteristics. *Forest Ecology and Management, 148*(1–3), 185–206. https://doi.org/10.1016/S0378-1127(00)00535-1
9. Köhler, P., & Huth, A. (1998). The effects of tree species grouping in tropical rainforest modelling: Simulations with the individual-based model FORMIND. *Ecological Modelling, 109*(3), 301–321. https://doi.org/10.1016/S0304-3800(98)00066-0
10. Laurance, W. F., Lovejoy, T. E., Vasconcelos, H. L., Bruna, E. M., Didham, R. K., Stouffer, P. C., Gascon, C., Bierregaard, R. O., Laurance, S. G., & Sampaio, E. (2002). Ecosystem decay of Amazonian forest fragments: A 22-year investigation. *Conservation Biology, 16*(3), 605–618. https://doi.org/10.1046/j.1523-1739.2002.01025.x
11. Monsi, M., & Saeki, T. (2005). On the factor light in plant communities and its importance for matter production (original work published 1953). *Annals of Botany, 95*(3), 549–567. https://doi.org/10.1093/aob/mci052
12. Naiman, R. J., Décamps, H., & McClain, M. E. (2005). *Riparia: Ecology, conservation, and management of streamside communities*. Elsevier Academic Press. ISBN 978-0-12-663315-3.
13. Phillips, O. L., & Gentry, A. H. (1994). Increasing turnover through time in tropical forests. *Science, 263*(5149), 954–958. https://doi.org/10.1126/science.263.5149.954
14. Poorter, L., Bongers, F., Aide, T. M., et al. (2016). Biomass resilience of Neotropical secondary forests. *Nature, 530*(7589), 211–214. https://doi.org/10.1038/nature16512
15. Winiwarter, L., Esmorís Pena, A. M., Weiser, H., Anders, K., Martínez Sánchez, J., Searle, M., & Höfle, B. (2022). Virtual laser scanning with HELIOS++: A novel take on ray tracing-based simulation of topographic full-waveform 3D laser scanning. *Remote Sensing of Environment, 269*, 112772. https://doi.org/10.1016/j.rse.2021.112772

### Software and tools

- **HELIOS++**: Heidelberg LiDAR Operations Simulator, 3DGeo Research Group, Heidelberg University. https://github.com/3dgeo-heidelberg/helios. It served as the conceptual reference for the LiDAR Cloud mode; it is not bundled or executed.
- **three.js** r128: 3D rendering library, MIT License. https://threejs.org
- **Tailwind CSS** 3.4.17: user-interface styling, MIT License. https://tailwindcss.com

## Files in this record

| File                                  | Content                                                                     |
| ------------------------------------- | --------------------------------------------------------------------------- |
| `forest_lab.html`                     | The simulator (single self-contained HTML file)                             |
| `README.md`                           | This description                                                            |
| `LICENSE.txt`                         | Copyright notice and terms of use                                           |
| `CITATION.cff`                        | Citation metadata (Citation File Format 1.2.0)                              |
| `forest_lab_01_forest_3d.png`         | Screenshot: 3D forest with the riparian corridor at year 150                |
| `forest_lab_02_lidar_point_cloud.png` | Screenshot: LiDAR Cloud mode at year 150                                    |
| `forest_lab_03_edge_effect.png`       | Screenshot: urban edge, the city next to the forest at year 300             |
| `forest_lab_04_urban_zone.png`        | Screenshot: urban zone with houses, buildings and factory smoke at year 300 |

## Copyright

© 2026 Jomil Costa Abreu Sales. All rights reserved. Third-party libraries remain under their own licenses. For permissions beyond those in `LICENSE.txt` (modification, redistribution, commercial or institutional use), contact the author through [ORCID](https://orcid.org/0000-0001-8722-8398) or [LinkedIn](https://www.linkedin.com/in/jomil-costa/).
