# Build History and Working Methods

## Recent Build Events

### 2025-01-18: Server Preservation Decision
- Action: Prevented modification of working fetch MCP server
- Reason: Core rules violation prevention
- Successful Steps:
  - Identified working component
  - Prevented modification
  - Documented decision
- Key Lesson: Working MCP servers must never be modified

### 2025-01-16: Data Collection Restoration
- Environment:
  - Python 3.13
  - Windows
  - Component Versions: All at 0.2.0
- Outcome: Successfully restored Raydium data collection
- Successful Steps:
  - Dependency installation
  - QuickNode connection test
  - Raydium collection test
- Issues Encountered:
  - Permission error during psutil installation
  - Unexpected unsubscribe response during cleanup
- Resolution: Fixed collector implementation and import paths

## Critical Working Methods

### 1. Component Modification Rules
- NEVER modify any completed components
- All completed components are READ ONLY
- New features must be implemented in new files only
- Maintain isolation of working components

### 2. Import Path Guidelines
- Keep existing import paths unchanged
- Follow consistent import patterns
- Do not "improve" working code patterns

### 3. Integration Practices
- Test new components in isolation first
- Verify against existing patterns
- Maintain component boundaries
- Follow exact working patterns

### 4. Error Recovery Protocol
- Revert changes to completed components immediately
- Roll back to last known working state
- Create new files instead of modifying existing ones
- Document all issues and resolutions

## Implementation Contradictions Found
1. Component Boundaries:
   - Original Plan: Strict component isolation
   - Current Reality: Some cross-component dependencies exist
   - Resolution: Maintain current dependencies, no new cross-component links

2. Import Patterns:
   - Design: Consistent import structure
   - Implementation: Mixed import styles across newer files
   - Action: Preserve existing styles, enforce consistency in new files only

3. Testing Approach:
   - Initial Plan: Fully isolated testing
   - Current State: Some integrated test dependencies
   - Solution: Keep existing test structure, isolate new tests only

## Working Methods Refinement

### DO:
- Create new files for new functionality
- Follow existing patterns exactly
- Test in isolation before integration
- Document all decisions and changes

### DON'T:
- Modify any working code
- Change import structures
- "Improve" existing patterns
- Create new cross-component dependencies

### ALWAYS:
- Check build_info.json before any changes
- Verify component status
- Follow existing patterns
- Document any contradictions found
