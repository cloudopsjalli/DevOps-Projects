# Secure Serverless API with AWS WAF, Monitoring & Auto-Response


## Architecture Diagram

![AWS Architecture](Secure-Server.png)



## Project Overview

This project demonstrates a **production-grade AWS serverless security architecture** that protects an API from malicious traffic, detects threats in real-time, and triggers automated alerts.

It showcases how to build a **multi-layered defense system** using:

* Edge protection
* Application-level filtering
* Monitoring & alerting

---

## Key Objectives

* Secure a serverless API from common web attacks
* Implement real-time traffic filtering using AWS WAF
* Monitor attack patterns using CloudWatch
* Trigger alerts via SNS when threats are detected
* Build a system that is **CV-ready and production aligned**

---


### Normal User Flow

User
  ↓
CloudFront
  ↓
API Gateway (HTTP API)
  ↓
AWS WAF
  ↓
Lambda
  ↓
DynamoDB


---

###  Attacker Flow (Detection & Blocking)

```
Attacker
  ↓
CloudFront + WAF
  ↓
🚫 Attack Blocked
  ↓
WAF Metrics
  ↓
CloudWatch
  ↓
CloudWatch Alarm
  ↓
SNS
  ↓
 Email Alert


## Security Features Implemented

* Rate limiting (DDoS protection)
* Edge-level filtering (CloudFront + WAF)
* Real-time attack detection
* Automated alerting system
* Logging and monitoring


---

 What you’ll learn:

- Cloud Front
- API Gateway
- Dynamo DB
- WAF2
- Cloud watch Alarm
############################################################################################################################
Author

Kalyan Jalli

Cloud & DevOps Engineer
Building real-world AWS architecture and automation projects.

GitHub: https://github.com/cloudopsjalli

License

This project is for educational purposes.

