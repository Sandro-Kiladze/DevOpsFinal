#!/bin/bash

echo "=== Docker Image Security Scan Report ===" > security/scan-results.txt
echo "Generated on: $(date)" >> security/scan-results.txt
echo "" >> security/scan-results.txt

# Build images first
docker-compose build

# Scan frontend image
echo "Scanning Frontend Image..." >> security/scan-results.txt
trivy image devops-pipeline-project-frontend:latest >> security/scan-results.txt
echo "" >> security/scan-results.txt

# Scan backend image
echo "Scanning Backend Image..." >> security/scan-results.txt
trivy image devops-pipeline-project-backend:latest >> security/scan-results.txt
echo "" >> security/scan-results.txt

echo "Scan completed. Results saved to security/scan-results.txt"