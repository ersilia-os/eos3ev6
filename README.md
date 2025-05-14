# CYP3A4 metabolism

Analysis of metabolic stability, determining the inhibition of CYP3A4 activity and whether the compounds are a substrate for the CYP3A$ enzyme. The data to build these models has been publicly available at PubChem (AID1645840, AID1645841, AID1645842) by ADME@NCATS.

This model was incorporated on 2023-07-06.

## Information
### Identifiers
- **Ersilia Identifier:** `eos3ev6`
- **Slug:** `ncats-cyp3a4`

### Domain
- **Task:** `Annotation`
- **Subtask:** `Activity prediction`
- **Biomedical Area:** `ADMET`
- **Target Organism:** `Not Applicable`
- **Tags:** `CYP450`, `ADME`, `Metabolism`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `2`
- **Output Consistency:** `Fixed`
- **Interpretation:** Probability of inhibiting the enzyme and probability of being a ubstrate of the enzyme. Activity in both indicates the compound is a ligand of the enzyme.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| cyp3a4_inhib | float | high | Probability of inhibition of the CYP3A4 |
| cyp3a4_subs | float | high | Probability of being metabolized by CYP3A4 |


### Source and Deployment
- **Source:** `Local`
- **Source Type:** `External`
- **DockerHub**: [https://hub.docker.com/r/ersiliaos/eos3ev6](https://hub.docker.com/r/ersiliaos/eos3ev6)
- **Docker Architecture:** `AMD64`, `ARM64`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos3ev6.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos3ev6.zip)

### Resource Consumption
- **Model Size (Mb):** `2506`
- **Environment Size (Mb):** `2447`


### References
- **Source Code**: [https://github.com/ncats/ncats-adme](https://github.com/ncats/ncats-adme)
- **Publication**: [https://dmd.aspetjournals.org/content/49/9/822](https://dmd.aspetjournals.org/content/49/9/822)
- **Publication Type:** `Peer reviewed`
- **Publication Year:** `2021`
- **Ersilia Contributor:** [ZakiaYahya](https://github.com/ZakiaYahya)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [None](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos3ev6
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos3ev6
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
