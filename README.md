# reviewsAPI
API gateway for performing CRD operations on GameShare sale data.

# build image: 
docker build . -t jackjackzhou/reviews-api

# run image though docker: 
docker run --publish 4005:4005 reviews-api

# push image:
docker push jackjackzhou/reviews-api

# kubectl create&run
minikube start
kubectl create -f reviews-app-deployment.yaml
minikube tunnel
minikube dashboard

# secret
kubectl create secret generic reviews-app-key --from-file=serviceAccountKey.json

kubectl describe secrets/reviews-app-key

# clean up
kubectl delete -f reviews-app-deployment.yaml