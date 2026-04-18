# How the Agent Works

> Moved to docs/guides/how-it-works.md

An operational explanation of every decision the system makes, from input to output.

---

## Overview

The agent processes a player message through four sequential steps before any response is generated:

1. **Classify** - what is the issue, how angry is the player, how confident are we
2. **Prioritize** - how urgent is this, what is the SLA
3. **Escalate** - should a human specialist handle this, and who
4. **Route** - what should the response say and collect
