# [2026] Senior Tech Lead - Hiring - Technical Interview
## Overview

We group our technical projects into Epics which are broken down into individual stories.

This take-home project presents an example epic with two stories. You should read and understand the requirements of the epic, and then:

1. [Review this Pull Request (PR)](https://github.com/runforsomething/senior-tech-lead-hiring-2026/pull/3) for the [first story](https://github.com/runforsomething/senior-tech-lead-hiring-2026/issues/1). Provide feedback on the PR to address bugs, potential optimizations, and how well the PR satisfies the story's requirements. You do not need to provide feedback on code style or other "nits" if they don't directly relate to these categories. We expect this to take 30 minutes; please spend no more than 45 minutes on this.

2. [Review the second story in the epic](https://github.com/runforsomething/senior-tech-lead-hiring-2026/issues/2), and write out a technical specification document (TSD) to provide direction to the engineerswho will implement it. [You can use this template](https://github.com/runforsomething/senior-tech-lead-hiring-2026/wiki/TSD-Template). We are not looking for specific implementation decisions in your TSD. Instead, we are interested in how you define and describe a non-trivial software system. We expect this to take about 1 hour; please spend no more than 90 minutes on this. Your TSD should provide direction on:

  1. Data models/data structures

  2. System design (particularly at the scale described)

  3. Recommendations on frameworks/tools/services to use, where you have a preference

  4. Other non-obvious parts of the implementation you would expect to see from the engineers implementing this story

For both tasks:

- We are not looking for completeness; just enough work that we have something substantial to discuss. Please do not feel a need to spend more than the recommended time on each.

- Feel free to use AI as you would if these tasks were assigned at work. Please be ready to discuss how and why you used AI if you do.

- We are here to answer questions! Please ask questions as github comments on the Pull Request for story 1, or on the issue for story 2. We'll reply within a few (working) hours.

To submit:

- Please submit your work by the night before your technical interview.

- Submit by sending an email to jordanhaines [at] runforsomething.net letting us know it's complete. You don't need to attach/submit anything since your work is all in Github.

## Epic Description

We have a lot of forms that people use to register for various things. Some of these forms we control, some are created by our partners but submit data to our backend. Currently, most of these forms are Jotforms or Airtable Forms from which we sync leads to our CRMs via Zapier automations. Every new form requires a new Zap, which is cumbersome to set up and more cumbersome to maintain. This is especially a challenge when partners create new forms as we have to coordinate connecting those external forms to our zaps individually. yuck.

The goal of this epic is to build a scalable, re-usable backend to accept leads posted from internal and external forms. First, we will build a generic endpoint that can capture and process a lead from any (well-structured) form. Then, we will scale that system. Ultimately, we need to be able to process up to 250K leads per day from hundreds of distinct forms.

Regardless of scale, it is very important for compliance reasons that we are able to report an accurate count of unique leads in real time. We need a persistent data view that our compliance team can access that contains no duplicate emails or phone numbers.

Assumptions:

- All forms that need to be submitted can post their payload to a webhook URL, and we can fully configure the payload within the form platform.
