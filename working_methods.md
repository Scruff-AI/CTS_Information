# Data Collection System - Working Methods

## Core Rules (MUST FOLLOW)

### 1. Component Preservation
- **NEVER** modify files marked as "completed" in build_info.json
- All completed components are strictly READ ONLY
- Working code patterns must be preserved exactly

### 2. Development Approach
- New features require new files only
- Zero modifications to existing working code
- Always check build_info.json before touching ANY file

### 3. Integration Rules
- Keep same import style as working code
- Test in isolation before integration
- Maintain component boundaries

## Workflow Sequence

### 1. Pre-Development Checks
- Review build_info.json for completed components
- Mark identified components as READ ONLY
- Plan new work to avoid touching completed components

### 2. Memory Verification
- Query build history for successful patterns
- Check for past failures and their causes
- Verify component status and dependencies

### 3. Implementation Process
- Create new files for new features
- Copy working patterns exactly
- Maintain isolation of working components

## Error Recovery Protocol

### 1. When Issues Occur
- Immediately revert any changes to completed components
- Roll back to last working state
- Create new files instead of fixing old ones

### 2. Prevention Measures
- Follow exact patterns that already work
- Use MCP workflow properly
- Maintain strict component isolation

## Windows-Specific Guidelines

### 1. Command Syntax
- Use PowerShell syntax
- Use semicolons not &&
- Quote paths with spaces
- Use correct path separators

### 2. File Operations
- Respect Windows path conventions
- Handle file permissions appropriately
- Consider Windows-specific dependencies

## Lessons Learned

### 1. From Build History
- Working MCP servers must never be modified
- New features require new files only
- Follow exact working patterns without changes

### 2. From Integration Tests
- Maintain isolation of working components
- Use consistent import paths
- Test thoroughly before integration

### 3. From Error Recovery
- Quick rollback is essential
- Document all issues and resolutions
- Learn from past failures

## Component Status (v0.2.0)

### Completed (READ ONLY):
1. Blockchain Integration
   - QuickNode Client
   - Raydium Collector
   - Integration Tests

2. Data Pipeline
   - Core Pipeline
   - Data Processing
   - Export System

3. Storage Layer
   - Database Implementation
   - Vector Store
   - Data Export

## Best Practices

### DO:
- Create new files for new functionality
- Follow existing patterns exactly
- Test in isolation
- Document all changes

### DON'T:
- Modify working code
- Change import structures
- "Improve" existing patterns
- Create cross-component dependencies

### ALWAYS:
- Check build_info.json first
- Verify component status
- Follow existing patterns
- Document decisions

## Implementation Checklist

1. **Before Starting**
   - [ ] Check build_info.json
   - [ ] Review completed components
   - [ ] Plan isolation strategy

2. **During Development**
   - [ ] Create new files only
   - [ ] Follow existing patterns
   - [ ] Test in isolation
   - [ ] Document changes

3. **Before Integration**
   - [ ] Verify no modifications to completed files
   - [ ] Check import paths match
   - [ ] Run isolated tests
   - [ ] Update documentation

4. **After Completion**
   - [ ] Verify working state
   - [ ] Document any issues
   - [ ] Update build information
   - [ ] Archive documentation
