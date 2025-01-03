# Flickr Analyzer

## Description
An analyzer script for the Flickr's photos.

It calculates the interest rate of the photos and results a sorted list of photos.

## How to run:
- Install the dependecies
```
pip install -r requirements.txt
```
- Create and fill in the env file (.env) with your Flickr's API_KEY & API_SECRET
```
FLICKR_API_KEY=<YOUR_API_KEY>
FLICKR_API_SECRET=<YOUR_API_SECRET>
```
- Also fill it in with the target's USER_ID
```
TARGET_USER_ID=<TARGET_USER_ID>
```
- Run the script
```
python fanalyze.py
```
