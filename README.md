# AHEAD
Interview preparation for applying to the start-up company AHEAD.


## Python Packages
I shall code in Python. As of 2023/07, following the suggestion on the latest
[`FlowCal` doc page](https://flowcal.readthedocs.io/en/latest/getting_started/install_anaconda.html)
- We are recommended to use Python version 3.8
- For packages used in this repo, refer to `requirements.txt`. In particular,
    - `FlowCal==1.3.0`, which already requires many dependencies like
      `matplotlib`, `numpy`, `openpyxl`, etc.

Alternatively, one could also install the current repo
- Either by
  ```shell
  $ pip install git+https://github.com/phunc20/ahead.git
  ```
- Or download the code and install from local
  ```shell
  $ pip install -e <downloaded_repos_local_path>
  $ # e.g. say you downloaded at ~/downloads/ahead, then it suffices to
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
        1. Use all 31 channels
        1. Use 31 channels with dimensionality reduction
        1. Suggested by `FlowCal`'s tutorial and by the problem description,
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


### Validation Set
Possessing cell samples from 40 patients, let's isolate 4 patients
(2 positive, 2 negative) to form our validation set. Besides,
let's choose those whose `(# events)` are intermediate.
- 2 positive: `flowrepo_covid_EU_034_flow_001` and `flowrepo_covid_EU_048_flow_001`
  with `98_608` and `123_154` events, resp.
- 2 negative: `flowrepo_covid_EU_013_flow_001` and `flowrepo_covid_EU_004_flow_001`
  with `170_075` and `183_001` events, resp.
