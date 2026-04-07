#!/bin/bash
# 1981 Content Worker - subprocess pi -p mode

cd /Users/yapex/workspace/warren_buffett_wiki

TASK_ID="22e6197d"
TEAM="wiki-1981"

# Mark task in progress
clawteam task update $TEAM $TASK_ID --status in_progress

# Run pi -p --no-session with task instructions from file
pi -p --no-session \
  --append-system-prompt "SCHEMA.md:$(cat SCHEMA.md)" \
  --append-system-prompt "letters/1977-letter.md:$(cat letters/1977-letter.md | head -50)" \
  "Process 1981 letter. Read SCHEMA.md from --append-system-prompt for format rules.

Do these steps:
1. Read raw/berkshire/1981-letter-en.md and raw/berkshire/1981-letter-zh.txt
2. Create letters/1981-letter.md - bilingual callout format (ZH/EN pairs)
3. Verify completeness (section headers, salutation, signature)
4. Create letters/1981-summary.md with frontmatter + sections
5. Create tmp/1981-entities.json with companies/people/concepts lists

Use existing company page names: ls companies/ and ls people/ and ls concepts/ to match exact filenames.

When done:
clawteam task update wiki-1981 22e6197d --status completed
clawteam inbox send wiki-1981 leader 'Completed 1981 letter processing'"