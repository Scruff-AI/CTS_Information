# Data Collection Minimal Testing Guide

## QuickNode Data Requirements

### Core Data Fields (DO NOT MODIFY)
```python
# Required trade data structure
{
    "signature": str,      # Transaction signature
    "timestamp": str,      # Transaction timestamp
    "type": str,          # Instruction type (e.g., "Swap")
    "data": {
        "slot": str,              # Block slot
        "success": bool,          # Transaction success
        "trader": str,            # Trader address
        "accounts": List[str],    # All involved accounts
        "writable_accounts": List[str],  # Writable accounts
        "readonly_accounts": List[str],  # Readonly accounts
    }
}
```

### Swap-Specific Fields (DO NOT MODIFY)
```python
# Additional fields for swap instructions
{
    "data": {
        "token_in": str,          # Input token mint
        "token_out": str,         # Output token mint
        "amount_in": float,       # Input amount
        "amount_out": float,      # Output amount
        "price": float,           # Calculated price
        "pool_id": str,          # Pool identifier
        "user_account": str      # User's token account
    }
}
```

## Minimal Testing Patterns

### 1. Reduced Output Testing
```python
# Use minimal logging in test handlers
async def minimal_trade_handler(trade_data: dict):
    """Minimal trade event handler to prevent terminal overflow"""
    try:
        # Log only essential data
        logger.info(f"Trade: {trade_data['type']}")
        logger.info(f"Signature: {trade_data['signature'][:8]}...")  # Truncate
        
        if "amount_in" in trade_data["data"]:
            logger.info(f"Amount: {trade_data['data']['amount_in']}")
    except Exception as e:
        logger.error(f"Handler error: {str(e)}")
```

### 2. Sample Test Commands
```bash
# Test with minimal output
python test_quicknode_live_minimal.py --log-level WARNING

# Test specific instruction type
python test_quicknode_live_minimal.py --instruction Swap

# Limited duration test
python test_quicknode_live_minimal.py --duration 60
```

### 3. Verification Checklist
- [ ] Connection established
- [ ] Subscription active
- [ ] Required data fields present
- [ ] Data types correct
- [ ] Handler receiving events

### 4. Testing Duration
- Short tests: 1-2 minutes
- Sample size: 5-10 trades
- Verify core fields only
- Stop after confirmation

## Working Patterns

### 1. Data Validation (DO NOT MODIFY)
```python
def validate_trade_data(data: Dict) -> bool:
    """Validate required trade data fields"""
    required_fields = {
        "signature": str,
        "timestamp": str,
        "type": str,
        "data": dict
    }
    
    required_data_fields = {
        "slot": str,
        "success": bool,
        "trader": str,
        "accounts": list
    }
    
    try:
        # Check top-level fields
        for field, field_type in required_fields.items():
            if field not in data:
                return False
            if not isinstance(data[field], field_type):
                return False
                
        # Check data fields
        for field, field_type in required_data_fields.items():
            if field not in data["data"]:
                return False
            if not isinstance(data["data"][field], field_type):
                return False
                
        return True
        
    except Exception:
        return False
```

### 2. Minimal Testing Handler
```python
class MinimalTestHandler:
    """Handler for minimal output testing"""
    
    def __init__(self):
        self.trade_count = 0
        self.start_time = time.time()
        self.max_trades = 10  # Limit sample size
        
    async def handle_trade(self, trade_data: Dict):
        """Process trade with minimal output"""
        self.trade_count += 1
        
        # Minimal logging
        logger.info(f"Trade {self.trade_count}/{self.max_trades}")
        
        # Stop after sample size
        if self.trade_count >= self.max_trades:
            logger.info("Sample size reached")
            return True  # Signal to stop
            
        return False
```

### 3. Test Execution
```python
async def run_minimal_test():
    """Run minimal test with limited output"""
    handler = MinimalTestHandler()
    quicknode = QuickNodeInput(ENDPOINT_URL)
    
    try:
        # Start with minimal logging
        logging.basicConfig(level=logging.WARNING)
        
        # Add minimal handler
        quicknode.add_trade_handler(handler.handle_trade)
        
        # Run for limited time
        await quicknode.start()
        await asyncio.sleep(60)  # 1 minute test
        
    finally:
        await quicknode.stop()
```

## Verification Guidelines

### 1. Essential Checks
- Connection successful
- Subscription active
- Data structure valid
- Types correct
- No errors

### 2. Skip Verification Of
- Extended trade details
- Market analysis
- Historical data
- Performance metrics

### 3. Quick Verification
1. Start test
2. Verify first trade data
3. Check required fields
4. Stop after confirmation

## Important Notes

### 1. Data Requirements
- DO NOT modify existing data structures
- DO NOT change field types
- DO NOT alter validation logic
- DO NOT extend required fields

### 2. Testing Approach
- Use minimal output
- Short test duration
- Small sample size
- Quick verification

### 3. Terminal Management
- Limit log levels
- Truncate long values
- Minimal status updates
- Essential errors only
