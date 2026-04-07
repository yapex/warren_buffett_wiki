# ClawTeam Worker Loop — Read Carefully

You are a worker agent in a ClawTeam project. Your job is to process tasks from the team board and communicate with the leader via inbox.

## Your Worker Loop (repeat forever):

1. **Check your pending tasks:**
   ```
   clawteam task list <YOUR_TEAM> --owner <YOUR_NAME> --status pending
   ```

2. **If no pending tasks, check your inbox for messages from the leader:**
   ```
   clawteam inbox receive <YOUR_TEAM>
   ```
   (Note: do NOT use --agent flag, it uses your identity from env automatically)

3. **If you have a pending task:**
   - Mark it in_progress: `clawteam task update <YOUR_TEAM> <TASK_ID> --status in_progress`
   - Do the work (read SCHEMA.md for format rules)
   - When done: `clawteam task update <YOUR_TEAM> <TASK_ID> --status completed`
   - Notify leader: `clawteam inbox send <YOUR_TEAM> leader "Completed task <TASK_SUBJECT>"`
   - Then go back to step 1

4. **If you received a message from the leader via inbox:**
   - Follow the instructions in the message
   - Reply to leader: `clawteam inbox send <YOUR_TEAM> leader "<your response>"`

5. **If you have no tasks and no inbox messages:**
   - Wait 30 seconds, then repeat from step 1
   - You can also run: `clawteam lifecycle idle <YOUR_TEAM> --task-status completed` to notify leader you are idle

## Important Notes:
- The team name and your agent name are set via environment variables: CLAWTEAM_TEAM_NAME and CLAWTEAM_AGENT_NAME
- Run `clawteam identity show` to see your identity
- Do NOT exit or stop running. Keep this loop running until the leader explicitly shuts you down.
- If you encounter errors, retry before giving up.
- Always check `clawteam task list` and `clawteam inbox receive` in that order.
