docker compose down || echo container
docker rm gatherone_oa || echo no image
docker build -t gatherone_oa .
docker compose up -d
