# Kanban Work Poller

The Kanban Work Poller is an automated service that continuously monitors kanban boards for ready tickets and automatically starts work on them when they become available.

## Features

- **Automatic Work Initiation**: Polls kanban boards at configurable intervals and automatically starts work on ready tickets
- **Intelligent Prioritization**: Uses the existing kanban prioritization system to select the highest-priority work
- **Documentation Integration**: Automatically triggers documentation stubs when work begins
- **Configurable Concurrency**: Controls how many work items can be started simultaneously
- **Multi-Board Support**: Can monitor multiple boards or all boards in the workspace
- **Graceful Shutdown**: Handles signals for clean service shutdown
- **Health Monitoring**: Provides status information and logging

## How It Works

1. **Polling**: The service polls configured kanban boards at regular intervals (default: 30 seconds)
2. **Discovery**: Uses `kanban_get_next_work` to find the highest-priority ready tickets
3. **Work Start**: Automatically moves selected tickets from "ready" to "in_progress"
4. **Documentation**: Triggers the documentation automation system to create feature stubs
5. **Tracking**: Keeps track of processed cards to avoid duplicate processing

## Configuration

The poller can be configured via command-line arguments or programmatically:

```bash
# Basic usage - poll all boards every 60 seconds, max 2 concurrent items
python santiago_core/services/kanban_work_poller.py

# Advanced configuration
python santiago_core/services/kanban_work_poller.py \
  --poll-interval 30 \
  --max-concurrent 3 \
  --boards board1 board2 \
  --no-docs
```

### Configuration Options

- `--poll-interval, -i`: Polling interval in seconds (default: 30)
- `--max-concurrent, -c`: Maximum concurrent work items (default: 3)
- `--boards, -b`: Target board IDs (default: all boards)
- `--no-docs`: Disable documentation automation
- `--dry-run`: Show what would be done without actually starting work
- `--status`: Show service status and exit

## Running as a Service

### Manual Control Script

Use the provided control script for easy service management:

```bash
# Start the poller
./kanban-poller.sh start

# Check status
./kanban-poller.sh status

# Stop the poller
./kanban-poller.sh stop

# Restart the poller
./kanban-poller.sh restart
```

### macOS Launchd Service

For automatic startup on macOS, load the launchd service:

```bash
# Load the service
launchctl load com.nusy-product-team.kanban-work-poller.plist

# Start the service
launchctl start com.nusy-product-team.kanban-work-poller

# Stop the service
launchctl stop com.nusy-product-team.kanban-work-poller

# Unload the service
launchctl unload com.nusy-product-team.kanban-work-poller.plist
```

## Testing

Run the test script to verify functionality:

```bash
python test_kanban_work_poller.py
```

This will:
1. Create a test board with sample tickets
2. Test the poller in dry-run mode
3. Optionally run a real test with actual work starting

## Integration with Kanban Workflow

The poller integrates seamlessly with the existing kanban workflow:

1. **Ticket Creation**: Tickets are created and moved to "ready" through normal kanban operations
2. **Automatic Start**: The poller detects ready tickets and starts work automatically
3. **Documentation**: Feature stubs are created automatically when work begins
4. **Progress Tracking**: Tickets move through the workflow as normal
5. **Completion**: When work is done, tickets are moved to "done" manually or through other automation

## Logging

The poller provides comprehensive logging:

- **Console Output**: Real-time status updates during operation
- **File Logging**: Logs are written to `logs/kanban-work-poller.out` and `logs/kanban-work-poller.err`
- **Structured Events**: Key events are logged with timestamps and context

Example log output:
```
2025-11-20 16:06:37,801 - KanbanWorkPoller - INFO - 📋 Found 2 ready ticket(s) on board test-work-poller
2025-11-20 16:06:37,801 - KanbanWorkPoller - INFO - 🚀 Starting work on: Implement user authentication
2025-11-20 16:06:37,809 - KanbanWorkPoller - INFO - ✅ Documentation triggered for Implement user authentication
```

## Safety Features

- **Duplicate Prevention**: Tracks processed cards to avoid starting work on the same ticket multiple times
- **Concurrency Control**: Limits the number of concurrent work items to prevent overload
- **Graceful Shutdown**: Responds to SIGINT/SIGTERM for clean shutdown
- **Error Handling**: Continues operation even if individual tickets fail to process
- **Dry Run Mode**: Allows testing without actually starting work

## Troubleshooting

### Common Issues

**Poller not finding tickets:**
- Check that tickets are in the "ready" column
- Verify board permissions and configuration
- Check logs for error messages

**Documentation not generating:**
- Ensure documentation integration is enabled (not using `--no-docs`)
- Check that the documentation service is properly configured
- Verify file system permissions for docs directory

**Service not starting:**
- Check Python path and virtual environment
- Verify all dependencies are installed
- Check log files for error details

### Monitoring

Use the status command to monitor the poller:

```bash
./kanban-poller.sh status
```

This shows:
- Whether the service is running
- Process ID and uptime
- Number of processed cards
- Recent log entries

## Architecture

The poller consists of several components:

- **KanbanWorkPoller**: Main service class handling polling logic
- **Board Discovery**: Automatic detection of available kanban boards
- **Work Selection**: Intelligent selection of ready tickets based on priority
- **Documentation Integration**: Triggers documentation automation on work start
- **State Management**: Tracks processed cards and service health

The service is designed to be lightweight and efficient, with minimal resource usage during polling operations.