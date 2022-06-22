# Google Kubernetes

### Skills and tools
`VK.Cloud` `terminal` `Ubuntu` `Kubectl` `Kubernetes` `Helm` `DOCKER` `S3` `Spark` `Spark Operator`  `Spark History Server`

---
### Task:
1. It is necessary to install `Spark Operator` in the `Kubernetes cluster`.
2. Use `Spark Operator` to run a test application to calculate the number of Pi.
3. Launch your application, which will read the data from `S3` and transfer it to another bucket in `S3`.
4. Install `Spark History Server` in `Kubernetes`.
5. Launch the `Spark` application, which will write logs to the `Spark History Server`.
6. Provide a screenshot from the `terminal` with the result of executing the command
kubectl get service -n spark-history-server

---
### Distributions versions: 

* Kubernetes 1.20.4, 
* spark-3.1.2-bin-hadoop3.2
* Ubuntu 20.04 

---
### Ход работы:
1. [*Kubectl Installation*][1] 
2. Helm Installation
3. Docker Installation
4. Spark Installation
5. Spark operator Installation
6. Spark Service account, role and role binding configuration
7. Spark demo example initiation
8. Custom app initiation
9. S3 Access account creation
10. s3 bucket creation
11. Spark History Server installation
12. Initiating Spark app with History Server support


[1]:https://github.com/Amboss/portfolio_projects/blob/master/google_kubernetes/scripts/work_progress.sh
