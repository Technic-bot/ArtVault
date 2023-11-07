# Art Vault 

"Art Vault" is an open source page designed to host and serve a gallery of artworks while providing an usable search functionality with minimal UI bloat. 
I initially created this as a way to host and serve 'Tom Fichbach' art in a gallery that is indexable and searchable, and is still the mains goal of this software, But should be able to be generalized to any art you want.

## Features and design goals.

1. Hosting art in a gallery type format.
2. Provide search functionality both via art title and tags. 
3. Simplicity, keep requirements and other dependencies at a minimun. 

## Architecture

Application consists on a React based Frontend created with npm-create-app 
plus Bulma for css, no other dependencies required,
you can find the frontend code on the aptly named vault_fronted folder. I have
very little frontend experience so if you want  to improve the look and feel, or
the quality of the JS code please send me a PR.

Frontend is data agnostic and simply queries a backend REST API. the code for this is 
located under the ArtVault directory and consist on a python flask application
backed by a sqlite database. Sqlite was chosen due to its flexibility, simplicity the
fact that there is very little artworks to serve. But system should be flexible
enough to use other more performant SQL database. But so far there is not need
for such change

## Requirements

Front end side you only need React.js and Bulma for css, the former of course
requires you to install node.js but other than that you only need to install
bulma

``` 
npm install bulma
```

For the back end you only need to install flask and gunicorn. But there is also a requirements file
on the repo top level you can use. I do recommend to create a virtual env for to
run this.

```
python -m venv vaultenv
source vaultenv/bin/activate
pip install -r requirements.txt
```

The flask app itself requires python 3.9 or higher to function.

## Running 

Running locally is relatively simple you just need to use npm and python, the
default config should point the frontend directly to the backend instance.

```bash
npm start
# Run on different terminal
python wsgi.py

```

For running on a server you can build the the frontend with the usual npm
command

```bash
npm run build
```

This will create an optimized build of the js code which you can zip and 
copy to your server.

```bash
cd vault_frontend
npm run build
zip -r vault.zip build
```

For the the backend you simply need to copy this repo and create a systemctl config file, an
example of this is provided on the config folder of this repo.

```bash
# Edit and copy .service file to your server
sudo systemctl enable artvault
sudo systemctl start artvault
```

If you are like me and are using a SELinux enabled distro to host this you may
need to add permissions for the virtualenv python executable to run. How to
enable this will depend on your config but you can base it on [this
gist](https://gist.github.com/Technic-bot/4c0184f29d155e31ca323d6cdd5ebde2)

## Artworks and Data

The flask back end does not serve the images themselves. The datbase stores the
relative path for each piece, plus metadata like title, post date, description,
 tags etc and simply returns a full URI to somewhere. This means you can host
 the images pretty much anywhere  and this separates the actual image storage
 from the application. Simplest solution for this is simply adding another
 location to your server where all images are stored. 

You can modify `instance/instance_config.py` to point to your actual image
storage location. Default is my dev PC internal ip but you can change it to your
website URL, or even point it to some object storage solution. 

You need to provide the actual file location and thumnail URI is also provided.
As gallery previews the artworks via the thumbnails and full sized images are
only served once user clicks on any link.

You can provide the images in any way you like, another advantage of separating 
the images storage from the app. But if you want to automatically get them from 
patreon and fill the database with the appropiate data you can use this project
sister repo
[PyPatreonHarvester](https://github.com/Technic-bot/PyPatreonHaverster)



