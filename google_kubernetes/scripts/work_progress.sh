

sudo apt-get update
# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# KUBECTL INSTALL
# https://mcs.mail.ru/docs/base/k8s/k8s-start/connect-k8s#section-2
# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# Установка с помощью встроенного пакетного менеджера Ubuntu, Debian или HypriotOS
sudo apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | \
sudo tee -a /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubectl
kubectl version --client
# >> Client Version: version.Info{Major:"1", Minor:"23", GitVersion:"v1.23.6" ...

#enabling autocomplete and using alias
sudo apt-get install bash-completion

nano ~/.profile

alias k=kubectl
source <(kubectl completion bash)
complete -F __start_kubectl k

# activating profile
source ~/.profile

# Create dir for kub config
mkdir -p $HOME/.kube
#sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

# Copy file to host
scp Downloads/kl_kubeconfig.yaml ubuntu@95.163.181.168:~/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
chmod 600 ~/.kube/config

# Check Kibernates cluster
kubectl cluster-info
kubectl cluster-info dump

# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# HELM INSTALL
# https://helm.sh/docs/intro/install/
# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | \
sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm

curl https://raw.githubusercontent.com/helm/helm/HEAD/scripts/get-helm-3 | bash
# >> helm installed into /usr/local/bin/helm
helm version
# >> version.BuildInfo{Version:"v3.8.2",

# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# DOCKER INSTALL
# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
#Set up the repository
#Update the apt package index and install packages to allow apt to use a repository over HTTPS:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
# >> Running hooks in /etc/ca-certificates/update.d...

#Add Docker’s official GPG key:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
# Update the apt package index, and install the latest version of
# Docker Engine and containerd, or go to the next step to install a specific version:
sudo apt-get update
# Docker install
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo docker run hello-world
# >>> Hello from Docker!

# Docker-compose install
sudo curl -L \
"https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" \
-o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
# >> docker-compose version 1.25.0, build 0a186604
# >> docker-py version: 4.1.0
# >> CPython version: 3.7.4
# >> OpenSSL version: OpenSSL 1.1.0l  10 Sep 2019


# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# SPARK INSTALL
# http://spark.apache.org/downloads.html
# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# Please note. For this tutorial i am using spark-3.1.2-bin-hadoop3.2

# Extract the Tarball
wget https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
tar -xvzf spark-3.1.2-bin-hadoop3.2.tgz

# add alias vars to profile for SPARK
nano ~/.profile
export SPARK_HOME=~/spark-3.1.2-bin-hadoop3.2
alias spark-shell=”$SPARK_HOME/bin/spark-shell”

# add alias vars to profile for Kibernates
#export KUBECONFIG=~/.kube/config

source ~/.profile
echo $SPARK_HOME
echo $KUBECONFIG

# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# SPARK OPERATOR INSTALL
# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
# >> "spark-operator" has been added to your repositories

# Here we install specific version (1.1.11) because on 26.11.2021
# last version has bugs and doesn`t work properly


helm install my-release spark-operator/spark-operator --namespace spark-operator \
--create-namespace --set webhook.enable=true --version 1.1.11
# >> NAME: my-release
# >> LAST DEPLOYED: Mon May  2 20:19:34 2022
# >> NAMESPACE: spark-operator
# >> STATUS: deployed
# >> REVISION: 1
# >> TEST SUITE: None


#helm upgrade --cleanup-on-fail \
#--install my-release spark-operator/spark-operator \
#--namespace spark-operator \
#--create-namespace \
#--set webhook.enable=true \
#--version 1.1.11 \
#--timeout 20m0s

k get ns
# >> NAME               STATUS   AGE
# >> default            Active   83m
# >> helm-deployments   Active   82m
# >> kube-node-lease    Active   83m
# >> kube-public        Active   83m
# >> kube-system        Active   83m
# >> opa-gatekeeper     Active   80m
# >> shell-operator     Active   77m
# >> spark-operator     Active   13m

#create service account, role and rolebinding for spark
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: spark-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["*"]
- apiGroups: [""]
  resources: ["services"]
  verbs: ["*"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: spark-role-binding
  namespace: default
subjects:
- kind: ServiceAccount
  name: spark
  namespace: default
roleRef:
  kind: Role
  name: spark-role
  apiGroup: rbac.authorization.k8s.io
EOF
# >> serviceaccount/spark created
# >> role.rbac.authorization.k8s.io/spark-role created
# >> rolebinding.rbac.authorization.k8s.io/spark-role-binding created



# Check Kibernates pod *  *  *  *  *  *  *  *  *  *  *  *  *  *
k get serviceaccount
# >> NAME           SECRETS   AGE
# >> dashboard-sa   1         38m
# >> default        1         39m
# >> spark          1         14s

k get roles.rbac.authorization.k8s.io
# >> NAME         CREATED AT
# >> spark-role   2022-04-29T11:58:40Z

k get rolebindings.rbac.authorization.k8s.io
# >> NAME                 ROLE              AGE
# >> spark-role-binding   Role/spark-role   35s

helm list --all-namespaces
# >> NAME            NAMESPACE       REVISION        UPDATED                                 STATUS      CHART                   APP VERSION
# >> STATUS       CHART                   APP VERSION
# >> gatekeeper      opa-gatekeeper  5               2022-05-02 12:43:51.729866504 +0000 UTC deployed     gatekeeper-3.7.0        3.7.0
# >> ingress-nginx   ingress-nginx   1               2022-05-02 12:40:31.3287316 +0000 UTC   deployed     ingress-nginx-4.0.17    1.1.1
# >> metrics-server  kube-system     1               2022-05-02 12:40:13.283099526 +0000 UTC deployed     metrics-server-5.9.2    0.5.0
# >> my-release      spark-operator  1               2022-05-02 13:04:30.250922563 +0000 UTC deployed     spark-operator-1.1.11   v1beta2-1.2.3-3.1.1

helm list --namespace spark-operator
# >> NAME            NAMESPACE       REVISION        UPDATED                                 STATUS      CHART                   APP VERSION
# >> my-release      spark-operator  1               2022-04-29 11:57:52.969871493 +0000 UTC deployed    spark-operator-1.1.11   v1beta2-1.2.3-3.1.1

# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# Run Spark demo example
# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
git clone https://github.com/GoogleCloudPlatform/spark-on-k8s-operator spark-operator
# Cloning into 'spark-operator'...
# >> remote: Enumerating objects: 6900, done.
# >> remote: Counting objects: 100% (65/65), done.
# >> remote: Compressing objects: 100% (42/42), done.
# >> remote: Total 6900 (delta 25), reused 42 (delta 16), pack-reused 6835
# >> Receiving objects: 100% (6900/6900), 24.42 MiB | 13.82 MiB/s, done.
# >> Resolving deltas: 100% (4772/4772), done.

ls -la
# >> drwxrwxr-x 13 ubuntu ubuntu      4096 May  2 11:53 spark-operator

k apply -f spark-operator/examples/spark-pi.yaml
# >> sparkapplication.sparkoperator.k8s.io/spark-pi created

k get sparkapplications.sparkoperator.k8s.io
# >> NAME       STATUS    ATTEMPTS   START                  FINISH       AGE
# >> spark-pi   RUNNING   1          2022-04-29T12:03:04Z   <no value>   21s

k get pods -n spark-operator
k describe my-release-spark-operator-5ffd7d5fb8-wzgt5 -n spark-operator

k describe sparkapplications.sparkoperator.k8s.io spark-pi
# >> Name:         spark-pi
# >> Namespace:    default
# >> Labels:       <none>
# >> Annotations:  <none>
# >> API Version:  sparkoperator.k8s.io/v1beta2
# >> Kind:         SparkApplication
# >> Metadata:
# >>   Creation Timestamp:  2022-04-29T12:02:59Z
# >>  ...
# >> Status:
# >>   Application State:
# >>     State:  RUNNING
# >>   Driver Info:
# >>     Pod Name:             spark-pi-driver
# >>     Web UI Address:       10.254.23.64:4040
# >>     Web UI Port:          4040
# >>     Web UI Service Name:  spark-pi-ui-svc
# >>   Execution Attempts:     1
# >>   Executor State:
# >>     spark-pi-123df380753421f1-exec-1:  PENDING
# >>   Last Submission Attempt Time:        2022-04-29T12:03:04Z
# >>   Spark Application Id:                spark-3f1e719810bb4ba1ac532eafbd60676c
# >>   Submission Attempts:                 1
# >>   Submission ID:                       e6aceb19-75de-4382-9de2-f01952657469
# >>   Termination Time:                    <nil>
# >> Events:
# >>   Type    Reason                     Age   From            Message
# >>   ----    ------                     ----  ----            -------
# >>   Normal  SparkApplicationAdded      63s   spark-operator  SparkApplication spark-pi was added, enqueuing it for submission
# >>   Normal  SparkApplicationSubmitted  58s   spark-operator  SparkApplication spark-pi was submitted successfully
# >>   Normal  SparkDriverRunning         54s   spark-operator  Driver spark-pi-driver is running
# >>   Normal  SparkExecutorPending       47s   spark-operator  Executor spark-pi-123df380753421f1-exec-1 is pending
# >>
# >>   Normal  SparkApplicationAdded      2m21s  spark-operator  SparkApplication spark-pi was added, enqueuing it for submission
# >>   Normal  SparkApplicationSubmitted  2m5s   spark-operator  SparkApplication spark-pi was submitted successfully
# >>   Normal  SparkDriverRunning         2m     spark-operator  Driver spark-pi-driver is running


k get pods
# >>> NAME                               READY   STATUS    RESTARTS   AGE
# >>> spark-pi-123df380753421f1-exec-1   0/1     Pending   0          3m13s
# >>> spark-pi-driver                    1/1     Running   0          3m25s

k logs spark-pi-driver | grep 3.1
# >>> 22/04/29 12:03:10 INFO SparkContext: Running Spark version 3.1.1
# >>> ...
# >>> Pi is roughly 3.1453357266786335

# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
# Running custom app
# *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
cd
git clone https://github.com/stockblog/webinar_spark_k8s/ webinar_spark_k8s

mv webinar_spark_k8s/custom_jobs/ $SPARK_HOME

# login to docker !!!!!!!!
sudo docker login

# Мы указали тег webinar_spark_k8s и Docker-файл:
sudo /$SPARK_HOME/bin/docker-image-tool.sh -r valknutt -t spark_k8s_intel -p ~/webinar_spark_k8s/yamls_configs/Dockerfile build
sudo /$SPARK_HOME/bin/docker-image-tool.sh -r valknutt -t spark_k8s_intel -p ~/webinar_spark_k8s/yamls_configs/Dockerfile push
# >> spark_k8s_intel: digest: sha256:08b241af6e9ae1893d67fc4c734e50b4e1a055f09d467958505cac4e0f12ec4b size: 4930
# >> valknutt/spark-r:spark_k8s_intel image not found. Skipping push for this image.

docker image ls
# docker image prune -a

# настройка Dockerfile
# https://mcs.mail.ru/help/ru_RU/s3-start/s3-account https://mcs.mail.ru/help/ru_RU/s3-start/create-bucket
# Для доступа в S3 требуется вручную внести jar драйвера
cd ~/webinar_spark_k8s/
cd yamls_configs$/
nano Dockerfile

# Creating Access acount

# создадим Secret, в нем будут храниться credentials
k create secret generic s3-secret \
--from-literal=S3_ACCESS_KEY=********** \
--from-literal=S3_SECRET_KEY=********************
k get secrets

# Creating s3 bucket name "my-s3"

# Create ConfigMap for accessing data in S3
k create configmap s3path-config \
--from-literal=S3_PATH='s3a://tbox/test.csv' \
--from-literal=S3_WRITE_PATH='s3a://tbox/write/test/'

k get configmaps
k describe configmaps s3path-config
#k delete configmaps s3path-config

# Launch spark job
#choose one of example yamls in directory yamls_configs, edit yaml, add your parameters such as docker repo, image, path to files in s3
k apply -f ~/webinar_spark_k8s/yamls_configs/s3read_write_with_secret_cfgmap.yaml

k get sparkapplications.sparkoperator.k8s.io
k describe sparkapplications.sparkoperator.k8s.io s3read-write-test
k get pods
k logs s3read-write-test-driver
k get events
k logs s3read-write-test-secret-cfgmap-driver


# Spark History Server

#create namespace for History Server
k create ns spark-history-server

#create secret so History Server could write to S3
k delete secrets/s3-secret -n spark-history-server

k create secret generic s3-secret \
--from-literal=S3_ACCESS_KEY=******************** \
--from-literal=S3_SECRET_KEY=****************************** \
-n spark-history-server
k get secrets -n spark-history-server

#create yaml file with config for History Server
#you should create bucket in S3 named spark-vt and directory inside bucket named spark-vt or change names in s3.logDirectory parameter

helm repo add stable https://charts.helm.sh/stable

helm install -f ~/webinar_spark_k8s/yamls_configs/values-hs.yaml \
my-spark-history-server stable/spark-history-server --namespace spark-history-server

helm upgrade \
--install -f ~/webinar_spark_k8s/yamls_configs/values-hs.yaml \
my-spark-history-server stable/spark-history-server \
--namespace spark-history-server
#WARNING: This chart is deprecated
#NAME: my-spark-history-server
#LAST DEPLOYED: Wed May  4 09:14:18 2022
#NAMESPACE: spark-history-server
#STATUS: deployed
#REVISION: 1
#TEST SUITE: None
#NOTES:
#Get the application URL by running the following commands. Note that the UI would take a minute or two to show up after the pods and services are ready.
#     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
#          You can watch the status by running 'kubectl -n spark-history-server get svc -w my-spark-history-server'
#  export SERVICE_IP=$(kubectl get svc --namespace spark-history-server my-spark-history-server -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
#     NOTE: If on OpenShift, run the following command instead:
#  export SERVICE_IP=$(oc get svc --namespace spark-history-server my-spark-history-server -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
#  echo http://$SERVICE_IP:map[name:http-historyport number:18080]

# Get External IP of History Server
k get service -n spark-history-server

# Launch Spark app with History Server support
cd ~/webinar_spark_k8s/yamls_configs
nano s3_hs_server_test.yaml

k apply -f ~/webinar_spark_k8s/yamls_configs/s3_hs_server_test.yaml

k get sparkapplications.sparkoperator.k8s.io
k describe sparkapplications.sparkoperator.k8s.io s3read-write-hs-server-test
k get pods
k logs s3read-write-hs-server-test
k get events s3read-write-hs-server-test
k describe pod s3read-write-hs-server-test-driver

# Для проверки задания пришлите скриншот из терминала с результатом выполнения команды
k get service -n spark-history-server
