## Changes Made 
 
### Improvement I-01 
Category: Context 
Problem: AGENTS.md was missing information
Change: Added sections: 
- `Before you start`, for errors caused due to nested folders
- `Read First`, to set a read orrder for the agent
- `Sources of truth`
- `Repository Map`, so that the agent can locate what it needs easily.
- `Standard Commands`, so that the agent does not invent commands
- `Change Rules`, so future changes don't affect negatively the code or documentation
- `Stop Conditions`, so the agent knows when to stop and ask for human intervention, to avoid the agent to take decisions that it shouldn´t do.
- `Validation` was updated to include the `verify.sh` script to avoid the agent to missing it out. 
Evidence: `AGENTS.md` updated.

 
### Improvement I-02 
Category: Tool-specific instructions 
Problem: There wasn't any tool for the agent used (Claude) 
Change: Added a `CLAUDE.md` with basic instructions and a redirection to `AGENTS.md`
Evidence: `CLAUDE.md` added. 

### Improvement I-03 
Category: Context  
Problem: The agent still struggled to locate everything it needed
Change: Added `REPO_MAP.md` to ease the location of everything in the project 
Evidence: `REPO_MAP.md` added.

### Improvement I-04 
Category: Script 
Problem: there wasn't a realiable way to make automated verifications on the project 
Change: Added `verify.sh` to automatize the verifications, the agent that execute tests, lint and a custom repository check with 1 command. 
Evidence: `scripts/verify.sh`

### Improvement I-05 
Category: Guardrail 
Problem: Relevant documentation could be missing and pointing to invalid dir's (due to lack of updated or human mistakes)
Change: Added a deterministic protected-path check taht validates existence of documents and that al directories in core documentation are valid. 
Evidence: Added `check_repo_contact.py`