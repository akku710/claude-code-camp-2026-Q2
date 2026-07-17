# Explore Agent Architectures

The largest confusion tech professionals have is applying the correct agent solution because many solutions appears to overlap responsibilities.

We will explore multiple agent architecture to determine fit for our agent workload.

## 1. An agent file with referenced files eg. AGENT.md, @~/docs/*.MD

The simplest agent is creating an "agent file" and possibly importing other files that are read conditionally when needed.

We should attempt to create an agent file and see if it can connect to the MUD and complete a simple goal:
eg. "Find the bakery and list the menu.

We want to use the the smallest and least intelligent model and scale up.

### Technical Observations

Using #gpt-5-mini

Observations:

- Coding harness wanted to read all files unrelated to instructions as well and was trying to find /bakery/menu folder structure.
- Agent created temp file scripts to create connection to MUD but failed at login, I asked to try with a persistent connection approach so it created 2 versions of proxy but result was still same.
- I gave agent manual output as well when I logged in using nc, still agent failed to successfully log in. 

