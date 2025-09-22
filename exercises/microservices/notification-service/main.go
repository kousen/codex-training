package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
)

func main() {
    r := gin.Default()

    r.GET("/health", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{
            "status":  "healthy",
            "service": "notification-service",
        })
    })

    // TODO: Implement notification handlers using Codex
    // - Connect to RabbitMQ
    // - Handle UserRegistered events
    // - Handle OrderCreated events
    // - Handle PaymentProcessed events
    // - Send emails/SMS notifications

    r.Run(":3003")
}