# Run first time only
git init -b main
gh auth login 
gh repo create demo-coral-iot
git pull --set-upstream origin main
git add . && git commit -m "initial commit" && git push


