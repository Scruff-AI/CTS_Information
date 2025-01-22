# Data Collection Working Methods

## Core Development Rules

### 1. Component Preservation
- **CRITICAL**: All v0.2.0 components are READ ONLY
- No modifications to existing working code
- New features must be implemented in new files
- Preserve exact working patterns

### 2. Implementation Process
1. Pre-Development
   - Check build_info.json for component status
   - Verify completed components
   - Plan isolation strategy
   - Review existing patterns

2. Development
   - Create new files only
   - Follow existing patterns exactly
   - Test in isolation
   - Document all changes

3. Integration
   - Verify no modifications to completed files
   - Match existing import patterns
   - Run isolated tests
   - Update documentation

### 3. Error Management
1. Prevention
   - Follow working patterns exactly
   - Use proper error handling
   - Implement comprehensive logging
   - Test edge cases

2. Recovery
   - Immediate rollback of changes
   - Return to last working state
   - Document issues and solutions
   - Update error patterns

## Implementation Guidelines

### 1. Code Organization
```python
# Follow this structure for new components
class NewComponent:
    # Constants at class level
    PROGRAM_ID = "..."
    INSTRUCTIONS = [...]
    
    def __init__(self):
        # Initialize with proper error handling
        try:
            self.setup_component()
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise
            
    async def start(self):
        # Proper startup sequence
        await self.connect()
        await self.subscribe()
        
    async def stop(self):
        # Clean shutdown
        await self.unsubscribe()
        await self.disconnect()
```

### 2. Error Handling Pattern
```python
# Use this pattern for all operations
try:
    # Main operation
    result = await self.process_data()
    
    # Validate result
    if not self.validate_result(result):
        raise ValueError("Invalid result")
        
    return result
    
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    await self.handle_connection_error()
    
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    await self.handle_general_error()
```

### 3. Testing Pattern
```python
# Standard test structure
@pytest.mark.asyncio
async def test_component():
    # Setup
    component = await setup_test_component()
    
    try:
        # Test operations
        result = await component.operation()
        
        # Assertions
        assert result.status == "success"
        assert len(result.data) > 0
        
    finally:
        # Cleanup
        await component.cleanup()
```

## Workflow Sequences

### 1. Adding New Features
1. Pre-Implementation
   - Review documentation
   - Check component status
   - Plan isolation approach
   - Design new files

2. Implementation
   - Create new files
   - Follow patterns exactly
   - Implement error handling
   - Add comprehensive logging

3. Testing
   - Unit tests first
   - Integration tests
   - Live environment tests
   - Performance verification

4. Documentation
   - Update technical docs
   - Add implementation notes
   - Document test cases
   - Update working methods

### 2. Error Recovery
1. Immediate Actions
   - Stop affected components
   - Log error details
   - Notify monitoring systems
   - Preserve error state

2. Analysis
   - Review error logs
   - Check component status
   - Verify data integrity
   - Identify root cause

3. Resolution
   - Create new files if needed
   - Implement fixes in isolation
   - Test thoroughly
   - Document solution

## Best Practices

### 1. Code Style
```python
# Follow these patterns
from typing import Dict, List, Optional

class ComponentName:
    """
    Clear class documentation with purpose and usage.
    Maintains isolation from other components.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize with typed parameters and documentation.
        
        Args:
            config: Configuration dictionary
        """
        self.validate_config(config)
        self.setup_component(config)
```

### 2. Documentation
```python
async def process_data(self, data: Dict) -> Optional[Dict]:
    """
    Process incoming data with clear documentation.
    
    Args:
        data: Input data dictionary
        
    Returns:
        Processed data or None if invalid
        
    Raises:
        ValueError: If data is malformed
        ConnectionError: If processing fails
    """
```

### 3. Testing
```python
# Test isolation pattern
@pytest.fixture
async def isolated_component():
    """Fixture providing isolated component instance"""
    component = TestComponent()
    try:
        await component.start()
        yield component
    finally:
        await component.stop()
```

## Maintenance Guidelines

### 1. Regular Checks
- Monitor error rates
- Review performance metrics
- Check resource usage
- Verify component isolation

### 2. Updates
- Document all changes
- Update test cases
- Maintain isolation
- Preserve patterns

### 3. Monitoring
- Track error patterns
- Monitor performance
- Check resource usage
- Verify data integrity

## Component Interaction Rules

### 1. Data Flow
```python
# Use this pattern for component interaction
class ComponentA:
    async def process(self, data: Dict):
        # Process in isolation
        result = await self.internal_process(data)
        
        # Pass to handler only
        for handler in self.handlers:
            await handler(result)
```

### 2. Error Propagation
```python
# Handle errors at component level
try:
    await self.process_data()
except ComponentError:
    # Handle known component errors
    await self.handle_component_error()
except Exception:
    # Log and stop component
    logger.error("Critical error")
    await self.stop()
```

### 3. Resource Management
```python
# Proper resource handling
async with self.resource_lock:
    try:
        await self.use_resource()
    finally:
        await self.cleanup_resource()
