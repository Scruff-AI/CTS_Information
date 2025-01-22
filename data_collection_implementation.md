# Data Collection Technical Implementation

## Code Structure

### Core Classes

#### 1. QuickNodeInput
```python
class QuickNodeInput:
    RAYDIUM_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
    TRADE_INSTRUCTIONS = ["Swap", "AddLiquidity", "RemoveLiquidity", ...]
    
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        self.subscriptions: Dict[str, int] = {}
        self.is_running = False
        self.retry_delay = 1
        self.max_retry_delay = 30
```

#### 2. HeliusInput
```python
class HeliusInput:
    RAYDIUM_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
    
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        self.request_semaphore = asyncio.Semaphore(10)  # Rate limiting
        self.request_interval = 1.0
```

#### 3. SwapInstructionParser
```python
@dataclass
class SwapInstruction:
    signature: str
    slot: int
    timestamp: str
    amount_in: float
    amount_out: float
    token_in_mint: str
    token_out_mint: str
    pool_id: str
    user_account: str
    success: bool
```

## Key Implementation Patterns

### 1. WebSocket Connection Management
```python
async def connect(self):
    while True:
        try:
            self.ws = await websockets.connect(self.endpoint_url)
            self.is_running = True
            asyncio.create_task(self._handle_messages())
            break
        except Exception as e:
            await asyncio.sleep(self.retry_delay)
            self.retry_delay = min(self.retry_delay * 2, self.max_retry_delay)
```

### 2. Rate Limiting Implementation
```python
async def _subscribe_to_logs(self):
    async with self.request_semaphore:  # Rate limit: 10 req/sec
        subscription_id = len(self.subscriptions) + 1
        request = {
            "jsonrpc": "2.0",
            "id": subscription_id,
            "method": "logsSubscribe",
            "params": [...]
        }
```

### 3. Message Processing
```python
async def _handle_messages(self):
    try:
        while self.is_running:
            message = await self.ws.recv()
            data = json.loads(message)
            
            if "method" in data and data["method"] == "logsNotification":
                processed_data = await self._process_log_notification(...)
                if processed_data:
                    for handler in self.trade_handlers:
                        await handler(processed_data)
    except websockets.exceptions.ConnectionClosed:
        self.is_running = False
```

### 4. Trade Event Processing
```python
async def _process_log_notification(self, log_data: Dict):
    if "logs" not in log_data:
        return None

    logs = log_data["logs"]
    transaction = log_data.get("transaction", {})
    
    for log in logs:
        if "Program log: Instruction:" in log:
            instruction = log.split("Instruction:")[1].strip()
            if any(instr in instruction for instr in self.TRADE_INSTRUCTIONS):
                return await self._parse_instruction(...)
```

## Error Handling Patterns

### 1. Connection Recovery
```python
def is_already_running():
    try:
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                os.remove(LOCK_FILE)
        return False
    except Exception:
        return False
```

### 2. Message Processing Errors
```python
try:
    processed_data = await self._process_log_notification(data["params"]["result"]["value"])
    if processed_data:
        for handler in self.trade_handlers:
            try:
                await handler(processed_data)
            except Exception as e:
                logger.error(f"Error in trade handler: {str(e)}")
except Exception as e:
    logger.error(f"Error handling messages: {str(e)}")
```

## Testing Implementation

### 1. Mock WebSocket
```python
class MockWebSocket:
    def __init__(self, messages=None):
        self.messages = messages or []
        self.sent_messages = []
        self.closed = False
        
    async def send(self, message):
        self.sent_messages.append(json.loads(message))
        
    async def recv(self):
        if self.messages:
            return json.dumps(self.messages.pop(0))
        raise ConnectionClosed(None, None)
```

### 2. Test Cases
```python
@pytest.mark.asyncio
async def test_connect_retry(quicknode_input):
    with patch('asyncio.sleep', AsyncMock()) as mock_sleep:
        with patch('websockets.connect', 
                  AsyncMock(side_effect=[Exception("Connection failed"), 
                                       MockWebSocket()])):
            await quicknode_input.connect()
            mock_sleep.assert_called_once_with(1)
            assert quicknode_input.is_running
```

## Performance Optimization

### 1. Message Queue Implementation
```python
self.message_queue = asyncio.Queue()  # Async message queue
await self.message_queue.put(data)    # Queue message
response = await self.message_queue.get()  # Process message
```

### 2. Resource Management
```python
async def stop(self):
    self.is_running = False
    if hasattr(self, 'ws'):
        if "logs" in self.subscriptions:
            try:
                request = {
                    "jsonrpc": "2.0",
                    "id": self.subscriptions["logs"],
                    "method": "logsUnsubscribe",
                    "params": [self.subscriptions["logs"]]
                }
                await self.ws.send(json.dumps(request))
            except Exception as e:
                logger.error(f"Error unsubscribing: {str(e)}")
        await self.ws.close()
    self.subscriptions.clear()
```

## Integration Points

### 1. Trade Handler Registration
```python
def add_trade_handler(self, handler: Callable):
    self.trade_handlers.append(handler)
```

### 2. Status Reporting
```python
def get_status(self) -> Dict:
    return {
        "is_running": self.is_running,
        "active_subscriptions": len(self.subscriptions),
        "monitored_program": self.RAYDIUM_PROGRAM_ID,
        "monitored_instructions": self.TRADE_INSTRUCTIONS,
        "trade_handlers": len(self.trade_handlers)
    }
```

## Configuration Constants

### 1. Program IDs
```python
RAYDIUM_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
RAYDIUM_AMM_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
```

### 2. Trade Instructions
```python
TRADE_INSTRUCTIONS = [
    "Swap",
    "AddLiquidity",
    "RemoveLiquidity",
    "CreatePool",
    "InitializePool",
    "Harvest",
    "Stake",
    "Unstake"
]
