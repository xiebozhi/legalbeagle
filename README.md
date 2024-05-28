# legalbeagle

28 May 2024

Legal Beagle is an idea for a project where we will build a legal Expert System, which is comprised of multiple Large Language Models (LLMs) that have been re-trained to be experts on on specific legal domains. 
This project is of intrest to Jason because in his work as a lawyer. And this is a personal passion project / portfolio item for Bobb who is considering a PhD in AI and watches too many youtube audits. 

We see two specific domains: criminal and civil.  Early in the project, we will concentrate specifically on criminal proceedings in South Carolina, as this is our first LLM project and we need a narrow focus so that we can learn.  In time, we expect this will be extended into every US state.  

We think there will be a priority / weight to data sources when referenced by the expert system: 
1) US Constitution
2) US Supreme Court Precedent
3) District Appellate Court Precedent
3.1) Possible fix for no prescedent in the district is to review/average presecent in other districts
4) Federal Laws
5) State Constitution
6) State Supreme Court Precedent
7) State District Court Precedent 
8) State Laws
9) Municipal Laws

Expert System Architecture:
-A primary / generalized LLM will talk to the human users, gather their information and evidence, ask clarifying questions and confirm mutual understanding of the case, then put those details through the apprpopriate expert sub-systems. 
-The primary LLM talks to defence and/or prosecution subsystems, which then decide the applicable jursidctions and works through the sub-systems by their priorities. 
-At this time, we think there should be an expert system for federal concerns, accompanied by 50+ for the states and territories. 
-This separation will prevent bleed over hallucenations where advice relevant in another state is errantly given to a user.
-Further fracturing of the expert sub-systems is possible when it makes sense to split the webcrawls and training into additional sub-systems.
-Explainability and citations are paramount. Hallucinations are to be squashed as best as possible. Ethically sourcing the data is a priority. 

Datasources:
Webcrawl for complete state and federal laws, starting with South Carolina due to Jason's status as a lawyer in the state. (Collaboration with lawyers in other states also likely in the future)
Webcrawl for Supreme Court cases, both Federal and State
Trial Manuals to describe trail processes, per state and federal district
Trial transcripts

Misc. Notes:
It is possible for state and federal charges to be pressed on the same defendant. But typically, the States drop their charges when Federal prosecution presses charges. 
We think it may take a state specific LLM to properly answer questions, due to the massive difference in state laws.  
- It’s a super common “joke” among criminal attorneys in the state, “Supreme Court overturned this.” “Yeah, but do you have a South Carolina case?"
- How to parse a Supreme Court case from a data structure standpoint? There are sometimes concurrences that are not controlling law and then dissents which could really undermine the understanding of a model
We want the ability, in a later version, to upload multiple videaos and have the AIs consider them as part of the evidence packet that goes through the expert systems for analysis. 

Want to help us code Legal Beagle?
We absolutely invite collaboration on this open source project, and will gladly consider providing access to those who have an interest in the legal aspect of this project, plus some experience that they could teach us, rather then us blindly leading the blind.  In the future, we might consider adding noobs that we are willing to teach, but we have to come up to speed first. 