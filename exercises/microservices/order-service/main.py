from fastapi import FastAPI

app = FastAPI(title="Order Service")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "order-service"}

# TODO: Implement order management endpoints using Codex
# - POST /api/orders - Create new order
# - GET /api/orders - List orders
# - GET /api/orders/{id} - Get order details
# - PUT /api/orders/{id}/status - Update order status
# - POST /api/orders/{id}/payment - Process payment

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3002)