echo "# example_repo" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:Lawrence-Hertzof/example_repo.git
git push -u origin main