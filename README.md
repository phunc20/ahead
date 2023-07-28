# AHEAD
Interview preparation for applying for the start-up company AHEAD.


## Quick Start
Here are a few quick ways to make use of the current repository
and the related ML models.
1. A tiny Swin Transformer model for image classification
   ```python
   In [1]: import FlowCal
      ...: import numpy as np
      ...: from ahead.util import get_fsc_ssc_chunks
      ...: from PIL import Image
      ...: from transformers import pipeline
   
   In [2]: pipe = pipeline(
      ...:     "image-classification",
      ...:     "phunc20/swin-tiny-patch4-window7-224-finetuned-wuhan")
   
   In [3]: file_flow_id = "flowrepo_covid_EU_013_flow_001"
      ...: fcs_path = next((data_dir/f'raw_fcs/{file_flow_id}').glob("*.fcs"))
   
   In [4]: chunk_generator = get_fsc_ssc_chunks(
      ...:     fcs_path,
      ...:     chunk_size=10_000,
      ...:     typ="A",
      ...:     gate_fraction=0.75,
      ...: )
   
   In [5]: chunk = next(chunk_generator)
      ...: chunk.shape
   Out[5]: (10000, 2)
   
   In [6]: FlowCal.plot.density2d(
      ...:     chunk,
      ...:     mode="scatter",
      ...:     savefig="chunk.png",
      ...: )
   
   In [7]: image = Image.open("chunk.png")
      ...: pipe(image)
   
   Out[7]: [{'score': 0.999931812286377, 'label': 'sick'},
      ...:  {'score': 6.822467548772693e-05, 'label': 'healthy'}]
   ```


## Python Packages
- Python version 3.8 is recommended by the
  [`FlowCal` doc page](https://flowcal.readthedocs.io/en/latest/getting_started/install_anaconda.html)
- And the packages inside `requirements.txt`
    - For Python newcomers, it suffices to
      ```shell
      $ pip install -r requirements.txt
      ```
    - In particular, `FlowCal` alone requires many dependecies, so it is highly possible that any package you need is included

Alternatively, instead of `requirements.txt`, one could also install the current repo (so that one could use
some of the repo's code)
- Either by
  ```shell
  $ pip install git+https://github.com/phunc20/ahead.git
  ```
- Or download the code and install from local
  ```shell
  $ pip install -e <downloaded_repos_local_path>
  $ # e.g. say you've downloaded (and unzipped) the repo at
  $ # ~/downloads/ahead
  $ # then it suffices to
  $ # pip install -e ~/downloads/ahead
  ```


## Take-Home Exam
### Difficulties
1. (# events) in each sample differs quite drastically
    - It could go as small as `680` events
    - Could also go as big as **several hundreds of thousand** events, e.g. `360_000`
1. Seemingly imbalanced binary classes (Sick/Healthy)


### Experiments
First come a few observations:
1. For each FCS file, We are given 35 channels, among which we are allowed to only
   use **31**, i.e. those whose `"use"` column is marked `1`
   in `EU_marker_channel_mapping.xlsx`
    - In this particular challenge, the **marker** information seems useless
      because including it won't bring any benefit.
    - As someone with almost no domain knowledge, I honestly do not know which of
      the 31 channels to discard/keep. I came up with 3 ways to proceed:
        1. [ ] Use all 31 channels
        1. [ ] Use 31 channels with dimensionality reduction
        1. [x] Suggested by `FlowCal`'s tutorial and by the problem description,
           maybe we could use FSC-SSC (gated) density plot to do some kind of
           image classification. In particular,
            - I shall not attempt to do calibration to MEF because we are not
              provided with calibration bead data
            - I do not see fluorescence channel either, so I will only focus on
              2D FSC-SSC density plots
            - If we choose to do this as an image classification task, then
              one immediate benefit is that even patients whose sample are
              of less number of events could be inferred using the same model
              (although the correctness of the inference is not guaranteed)
        1. [ ] As an alternative to the previous, i.e the 3rd way, aside from
            - FSC-A vs SSC-A
            - FSC-W vs SSC-W
            - FSC-H vs SSC-H
           we could have tried all sorts of 2D density plots invovling all the
           combinations of the `31` channels, i.e. roughly 31 choose 2 combinations
1. As mentioned in the above subsection, the number of events varies quite a lot.
   Consequently, I decide to group
    - 500
    - 1,000
    - 5,000
    - 10,000
   
   events together to make up an instance.  
   By doing so,
    - Not only do we increase the number of samples/instances
    - But it also enables us to do prediction when future data come
      in small number of events
   
   This should be similar to sliding windows. To make things simple,
   I **choose not to have the windows overlap one another**.

**Rmk.**
- At the end, I do not find enough time to do all the listed experiments


### Validation Set
Possessing cell samples from 40 patients, let's isolate 4 patients
(2 sick, 2 healthy) to form our validation set. Besides,
let's choose those whose `(# events)` are intermediate.
- 2 sick: `flowrepo_covid_EU_034_flow_001` and `flowrepo_covid_EU_048_flow_001`
  with `98_608` and `123_154` events, resp.
- 2 healthy: `flowrepo_covid_EU_013_flow_001` and `flowrepo_covid_EU_004_flow_001`
  with `170_075` and `183_001` events, resp.


### Code
Most of my developped code are in
- `docs/notebooks/`
- and `ahead/`

Because I developped the code on a very
old laptop (Thinkpad X61s with Intel(R)
Core(TM)2 Duo CPU, to be more precise),
most of the code I wrote I ran on Colab.
Sorry for not devoting more time on
converting them into Python script.

But from another point of view, since
most of the code carries experiment
smells, i.e. nothing really of
production-ready, so I think it isn't
so bad that they were in
Jupyter-notebook form.


## Bonus Question
By reading the question description
and by reading `FlowCal`'s tutorials
side-by-side, it's hard to not have
suspected that the gating techniques
introduced in
<https://flowcal.readthedocs.io/en/latest/python_tutorial/gate.html>
may help with the bonus question.
In particular, the
`FlowCal.gate.density2d`
helps reduce manual works to only one
input arg: `gate_fraction`.
I think it could be considered automatic.
