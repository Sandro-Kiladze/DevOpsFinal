#!/bin/bash

echo "=== Incident Simulation Started ===" | tee incident/incident-log.txt
echo "Time: $(date)" | tee -a incident/incident-log.txt
echo "" | tee -a incident/incident-log.txt

echo "Step 1: Recording baseline metrics..." | tee -a incident/incident-log.txt
curl -s http://localhost:5000/health | tee -a incident/incident-log.txt
curl -s http://localhost:5001/api/health | tee -a incident/incident-log.txt
echo "" | tee -a incident/incident-log.txt

echo "Step 2: Simulating backend failure..." | tee -a incident/incident-log.txt
docker-compose stop backend
echo "Backend container stopped at $(date)" | tee -a incident/incident-log.txt
echo "" | tee -a incident/incident-log.txt

echo "Step 3: Monitoring system behavior for 60 seconds..." | tee -a incident/incident-log.txt
for i in {1..12}; do
    echo "Check $i at $(date):" | tee -a incident/incident-log.txt
    curl -s http://localhost:5000/health || echo "Frontend unreachable" | tee -a incident/incident-log.txt
    curl -s http://localhost:5001/api/health || echo "Backend unreachable" | tee -a incident/incident-log.txt
    sleep 5
done

echo "" | tee -a incident/incident-log.txt
echo "Step 4: Restoring service..." | tee -a incident/incident-log.txt
docker-compose start backend
echo "Backend container restarted at $(date)" | tee -a incident/incident-log.txt

echo "" | tee -a incident/incident-log.txt
echo "Step 5: Verifying recovery..." | tee -a incident/incident-log.txt
sleep 10
curl -s http://localhost:5000/health | tee -a incident/incident-log.txt
curl -s http://localhost:5001/api/health | tee -a incident/incident-log.txt

echo "" | tee -a incident/incident-log.txt
echo "=== Incident Simulation Completed ===" | tee -a incident/incident-log.txt