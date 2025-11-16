# Copilot Auto Approve Settings Guide

To enable automatic approval of Copilot commands in VS Code, follow these steps:

1. Open VS Code Settings (Cmd/Ctrl + ,)
2. Search for "copilot auto approve"
3. Configure the following settings:

## Terminal and Tool Auto Approval Settings

- **chat.tools.edits.autoApprove**: Enable and add commands like `git`, `gh`, and any other commands you want auto-approved
- **chat.tools.global.autoApprove**: Enable
- **chat.tools.terminal.autoApprove**: Add other commands in the linked settings.json file
- **chat.tools.terminal.enableAutoApprove**: Enable
- **chat.tools.terminal.ignoreDefaultAutoApproveRules**: Leave unenabled unless nothing else works

## Additional Copilot Settings

- **github.copilot.chat.agent.autoFix**: Enable
- **github.copilot.renameSuggestions.triggerAutomatically**: Enable

After configuring these settings, restart VS Code for changes to take effect. This will allow Copilot to execute approved commands automatically without requiring manual approval each time.
