docker build -t demo-convert2pdf .
docker tag demo-convert2pdf us-central1-docker.pkg.dev/gsd-ai-mx-ulises/cloudrun-images/demo-convert2pdf:latest
docker push us-central1-docker.pkg.dev/gsd-ai-mx-ulises/cloudrun-images/demo-convert2pdf:latest

gcloud run deploy demo-convert2pdf \
--image us-central1-docker.pkg.dev/gsd-ai-mx-ulises/cloudrun-images/demo-convert2pdf:latest \
--platform managed \
--region us-central1 \
--port 8080 \
--allow-unauthenticated 